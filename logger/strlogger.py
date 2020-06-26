import logging.config

logging.config.fileConfig(fname='logger/logger.conf', disable_existing_loggers=True)
strlogger = logging.getLogger(__name__)

logger_dict = {
    "DEBUG": strlogger.debug,
    "INFO": strlogger.info,
    "WARNING": strlogger.warning,
    "ERROR": strlogger.error,
    "CRITICAL": strlogger.critical
}
