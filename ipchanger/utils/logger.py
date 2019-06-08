import logging
from definitions import ROOT_DIR


class Logger:
    """class Logger to set up a Logger instance

    USAGE:
            Logger(name='ipchanger', level=logging.INFO)

    """
    def __init__(self, name='ipchanger', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        str_handler = logging.StreamHandler()
        str_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(message)s')
        str_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(ROOT_DIR + '/ipchanger.log', mode='a')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(str_handler)
        self.logger.addHandler(file_handler)

    def info(self, msg):
        """logs info messages

        :param msg: string messages
        """
        self.logger.info(msg)

    def debug(self, msg):
        """logs debug messages

        :param msg: string messages
        """
        self.logger.debug(msg)

    def warning(self, msg):
        """logs warning messages

        :param msg: string messages
        """
        self.logger.warning(msg)

    def error(self, msg):
        """logs error messages

        :param msg: string messages
        """
        self.logger.error(msg)
