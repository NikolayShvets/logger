"""
Модуль, инициализирующий объект логгера из модуля <logging>
в соответствии с параметрами из <logger/logger.conf>
"""
import logging.config

logging.config.fileConfig(fname="logger/logger.conf", disable_existing_loggers=True)
str_logger = logging.getLogger(__name__)

# словарь функций логгера, ключи - уровни сообщения
logger_dict = {
    "DEBUG": str_logger.debug,
    "INFO": str_logger.info,
    "WARNING": str_logger.warning,
    "ERROR": str_logger.error,
    "CRITICAL": str_logger.critical
}
