import logging
import os
from time import strftime, gmtime

def create_log():
    log_time_stamp = strftime('%Y%m%d_%H%M%S')
    os.mkdir(f'Logs\\{log_time_stamp}\\')
    os.mkdir(f'Logs\\{log_time_stamp}\\screenshots\\')

    # Log Directory
    LOG_DIR = f'Logs\\{log_time_stamp}\\'
    # 
    LOG_FILENAME = f'Log_{log_time_stamp}.log'

    logging.basicConfig(
        filename=LOG_DIR + LOG_FILENAME, 
        encoding='utf-8', level=logging.INFO
    )

    return f'Logs\\{log_time_stamp}\\screenshots\\'

def write_to_log(LOGGER, level, message):
    if level == 'DEBUG':
        LOGGER.debug(message)
    elif level == 'INFO':
        LOGGER.info(message)
    elif level == 'WARNING':
        LOGGER.warning(message)
    elif level == 'ERROR':
        LOGGER.error(message)
