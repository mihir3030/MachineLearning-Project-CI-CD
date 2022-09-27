# this file is use for create logging information
import logging
from datetime import datetime
import os

# define formate of log_file
LOG_DIR = "logs"
current_time_stamp = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
logfile_name = f"log_{current_time_stamp}.log"

# create directory for log folder
os.makedirs(LOG_DIR, exist_ok=True)

# join folder and file name to file path
LOG_FILE_PATH = os.path.join(LOG_DIR, logfile_name)

# create format of logging info
logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format='[%(asctime)s]-%(levelname)s-%(filename)s-%(lineno)d-%(funcName)s()--%(message)s',
level=logging.INFO
)
