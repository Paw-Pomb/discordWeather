import os
import logging

class Logger:
    def setLogger(logger_name):
        if logger_name not in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            log_dir = os.path.join(os.path.dirname(__file__), "logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file_path = os.path.join(os.path.dirname(__file__), "logs/bot.log")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s")
            file_handler = logging.FileHandler(log_file_path, mode='a')
            file_handler.setFormatter(formatter)
            if not logger.handlers:
                logger.addHandler(file_handler)
            return logger
        return logging.getLogger(logger_name)