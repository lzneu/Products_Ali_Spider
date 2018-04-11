import logging
# from ..config import config
# from Config.config import config

log_level = 'info'
log_file_name = 'test.log'


def get_logger(log_level):
    formatter_str ='%(asctime)s %(levelname)s [%(processName)s] [%(threadName)s] - %(message)s'
    formatter = logging.Formatter(formatter_str)
    logging.basicConfig(level=logging.DEBUG,
                        format=formatter_str)

    Logger = logging.getLogger()

    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)
    Logger.addHandler(file_handler)

    if log_level == 'debug':
        level = logging.DEBUG
    elif log_level == 'info':
        level = logging.INFO
    else:
        level = logging.WARNING
    Logger.setLevel(level)
    return Logger


Logger = get_logger(log_level)
