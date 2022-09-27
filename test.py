from housing.logger import logging
from housing.exception import HousingException
import sys


try:
    raise Exception("testing custom error")
except Exception as e:
    housing = HousingException(e, sys)
    logging.info(housing.error_message)
    logging.info("we are testing logging function")
