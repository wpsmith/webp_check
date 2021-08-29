import logging

logging.basicConfig(filename='logs.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
