import logging
import logging.config

logging.config.fileConfig(fname='logger/logger.conf', disable_existing_loggers=True)
strlogger = logging.getLogger(__name__)
