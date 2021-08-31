import logging
import os

import config

logpath = config.get().get('LOG_PATH')
if logpath is None or "" == logpath:
    logpath = "."

logfile = os.path.join(logpath, "logs.log")
logging.basicConfig(filename=logfile, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
