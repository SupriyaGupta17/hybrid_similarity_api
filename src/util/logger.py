"""
    get_logger.py
    ~~~~~~
    Created By : Pankaj Suthar
"""
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler


class ApplicationLogger:
    """ Logger Class """

    def __init__(self, logs_dir, logs_backup_count):
        """
        Constructor
        :param logs_dir: Logs Directory
        :param logs_backup_count: Logs backup count
        """
        self.logs_dir = logs_dir
        self.logs_backup_count = logs_backup_count

    def __create_logger_instance(self):
        """
        __create_logger_instance
        :return: Logger Object
        """
        # Create directory if not exist
        if not os.path.isdir(self.logs_dir):
            os.makedirs(self.logs_dir)
        logger = logging.getLogger("ApplicationLogger")
        log_handler = TimedRotatingFileHandler(self.logs_dir + "/execution.logs",
                                               when="D",
                                               interval=1,
                                               backupCount=self.logs_backup_count,
                                               atTime=datetime.time(11, 45, 00))

        formatter = logging.Formatter('%(asctime)s -[%(levelname)s]- %(message)s ')
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(logging.ERROR)
        logger.setLevel(logging.INFO)
        logger.info("Application Logs Initialized")
        return logger

    @property
    def get_logger(self):
        """
        Property: Provide Logger
        :return: get_logger Object
        """
        return self.__create_logger_instance()
