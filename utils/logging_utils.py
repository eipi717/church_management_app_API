import logging


class Logger:
    name: str
    level: str

    def __init__(self, name: str, level: str):

        # Remove the ".py" from the file name
        self.name = name.split(".py")[0]
        self.level = level

    def create_logger(self):
        """
        Create logger object based on the script name and log level
        :return: logger object
        """
        logger = logging.getLogger(f'{self.name}_{self.level}')
        logger.setLevel(self.level)

        # Save the log to specific file
        log_file = logging.FileHandler(f'{self.level.lower()}.log')
        log_file.setLevel(self.level)

        # Formatting the log
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
        log_file.setFormatter(formatter)

        logger.addHandler(log_file)

        return logger
