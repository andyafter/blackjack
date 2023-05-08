import logging

class Logger:
    def __init__(self, logger_name, log_file=None, log_level=logging.INFO, log_target='both'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if log_target in ('file', 'both') and log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if log_target in ('console', 'both'):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def enable_logging(self):
        self.logger.setLevel(logging.DEBUG)

    def disable_logging(self):
        self.logger.setLevel(logging.CRITICAL + 1)

    def get_logger(self):
        return self.logger
