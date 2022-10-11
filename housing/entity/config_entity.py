from collections import namedtuple

# this is data_ingestion_config to provide data_url path and data_save path
DataIngestionConfig = namedtuple("DataIngestionConfig", 
["dataset_download_url", "tgz_download_dir", "raw_data_dir", "ingested_train_dir", "ingested_test_dir"])


# this is data_validation schema  specify numbers of columns and data_type
DatavalidationConfig = namedtuple("DataValidationConfig", ['schema_file_path'])


"""  FeatureEngineering Step
this TransformationConfig is used for feature_engineering
'add_bedroom_per_room' -- add new column in feature_enginnering step
'transformed_train_dr' -- after applied feature_engineering in train_data save transformed data to this path
'transformed_test_dir' -- after applied feature_engineering in test_data save transformed data to this path
'preprocessed_object_file_path' -- save pickle file for any object Ex.. StandardScaler pickle file
"""
DataTransformtionConfig = namedtuple("DataTransformationConfig", ['add_bedroom_per_room',
                                                                  'transformed_train_dr',
                                                                  'transformed_test_dir',
                                                                  'preprocessed_object_file_path'])


# after ModelTraining save model path 
# base accuracy if my new model is not giving accuracy better than base accuracy we will not accept new model
ModelTrainingConfig = namedtuple("ModelTrainingConfig", ['trained_model_file_path', 'base_accuracy'])


#
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ['model_evaluation_file_path', 'timeS_stamp'])


# where to push the model path
ModelPusherConfig = namedtuple("ModelPusherConfig", ['export_dir_path'])


#
TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ['artifact_dir'])