import os
import sys
import pandas as pd
import numpy as np
from housing.entity.config_entity import DataIngestionConfig
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile  # with help we can extract zip file
from six.moves import urllib  # with help we can download data
from sklearn.model_selection import StratifiedShuffleSplit



class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion log started {'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e, sys) from e


    # this function is used for dowload data from net
    def download_housing_data(self) -> str:
        try:
            # download url
            download_url = self.data_ingestion_config.dataset_download_url

            # folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            # create directory for zip file
            os.makedirs(tgz_download_dir, exist_ok = True)

            # give the name of zip file from URL
            housing_file_name = os.path.basename(download_url)

            # give directory and file name to generate exact path
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            # download file
            logging.info(f"Downloading File from: {download_url} into {tgz_file_path} ")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"Downloading dataset compleated into {tgz_file_path} ")
            
            return tgz_file_path
        
        except Exception as e:
            raise HousingException(e, sys) from e


    # this function is used to extract zip file into raw_data dir
    def extract_tgz_data(self, tgz_file_path: str):
        try:
            # get path of raw_data_dir to save extrcted data
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # make raw_data dir
            os.makedirs(raw_data_dir)

            # extract data
            logging.info(f"Extracting tgz_file: {tgz_file_path} into: {raw_data_dir}")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path = raw_data_dir)
            logging.info(f"Extracting tgz_file is compleated at: {raw_data_dir}")

        except Exception as e:
            raise HousingException(e, sys) from e


    # this function is used for split data into train and test dir
    def split_data_train_test(self) -> DataIngestionArtifact:
        try:
            # get our dataset file 
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # we don't know the exact extracted filename with help of this we can get dataset filename
            file_name = os.listdir(raw_data_dir)[0]

            # this gives us our dataset file_name path to load data into pandas
            housing_file_path = os.path.join(raw_data_dir, file_name )

            # load dataset into dataframe
            logging.info(f"reading csv file from - {housing_file_path}")
            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame['income_cat'] = pd.cut(
                housing_data_frame['median_income'],
                bins=[0.0, 1, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )

            logging.info(f"splitiing data into train test")
            start_train_set = None
            start_test_set = None

            split = StratifiedShuffleSplit(n_splits = 1, test_size=0.3, random_state = 33)

            for train_index, test_index in split.split(housing_data_frame, housing_data_frame['income_cat']):
                start_train_set = housing_data_frame.loc[train_index].drop(['income_cat'], axis=1)
                start_test_set = housing_data_frame.loc[test_index].drop(['income_cat'], axis=1)
                
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if start_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok = True)
                logging.info(f"Exporting training dataset to file - {train_file_path}")
                start_train_set.to_csv(train_file_path, index=False)

            if start_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok = True)
                logging.info(f"Exporting testing dataset to file - {test_file_path}")
                start_test_set.to_csv(test_file_path, index = False)


            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path, test_file_path = test_file_path,
                                is_ingested=True, message=f"Data Ingestion  compleated successfully")

            logging.info(f"Data Ingestion Artifact - {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise HousingException(e, sys) from e


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_data(tgz_file_path = tgz_file_path)
            return self.split_data_train_test()
        except Exception as e:
            raise HousingException(e, sys) from e


    def __del__(self):
        logging.info(f"{'='*20} Data Ingestion log completed {'='*20}")
