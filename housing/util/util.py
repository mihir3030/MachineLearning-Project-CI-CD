import os
import yaml
from housing.exception import HousingException
import sys


# this function is use for load and read yaml file
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb')as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e, sys) from e