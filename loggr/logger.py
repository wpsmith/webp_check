import logging
import os

import config

logfile = os.path.join(config.get().get('LOG_PATH'), "logs.log")
logging.basicConfig(filename=logfile, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
