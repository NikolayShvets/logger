"""
Модуль, инициализирующий объект логгера из модуля <logging>
в соответствии с параметрами из <logger/logger.conf>
"""
import logging.config

logging.config.fileConfig(fname='logger/logger.conf', disable_existing_loggers=True)
strlogger = logging.getLogger(__name__)

# словарь функций логгера, ключи - уровни сообщения
logger_dict = {
    "DEBUG": strlogger.debug,
    "INFO": strlogger.info,
    "WARNING": strlogger.warning,
    "ERROR": strlogger.error,
    "CRITICAL": strlogger.critical
}
