# -*- coding: utf-8 -*-
"""
Модуль логгирования. Инициализирует статический класс логгера
с методом - декоратором, записывающим лог в базу данных, по указанному URI
в файле настроек <config.py>
"""

from logger import loggerThread
from logger.strlogger import strlogger
from functools import wraps
from logger.models.logTablesModels import LogJournal, Session, tracing_depth
from datetime import datetime
import traceback
import re


class logger:
    @loggerThread.logger_thread
    def write_log(**kwargs: list) -> None:
        """
        Метод, открывающий покдлючение к базе данных логера
        и записывающий лог в базу данных
        :param kwargs: list
        :return: None
        """

        DBSession = Session()
        DBSession.add(LogJournal(**kwargs))
        DBSession.commit()

    @staticmethod
    def strlog(message: str, level: str = "DEBUG", exc_info=False):
        """
        Метод для логгирования внутри оборачиваемых функций.

        :param exc_info: флаг исключения
        :param message: строка сообщения
        :param level: уровень сообщения
        :return: None
        """

        if exc_info:
            strlogger.exception(message)
            return
        if level == "DEBUG":
            strlogger.debug(message)
        elif level == "INFO":
            strlogger.info(message)
        elif level == "WARNING":
            strlogger.warning(message)
        elif level == "ERROR":
            strlogger.error(message)
        elif level == "CRITICAL":
            strlogger.critical(message)


    @staticmethod
    def build_log_with_message(session: dict):
        """
        Метод, передающий сессиию flask в декортаор логгирования
        :param session: словарь сессии flask
        :return: декоратор над переданной функцией
        """
        def build_log(func):
            @wraps(func)
            def build_log_wrapper(*args: tuple, **kwargs: list):
                """
                Обертка над переданной функцией func.
                :param args: кортеж неименованных аргументов.
                :param kwargs: список именованных аргументов.
                :return: результат работы оборачиваемой функции func
                """

                data = {}
                data.update(dict(session))
                data.update(func.__apidoc__["responses"])
                print(data)
                try:
                    result = func(*args, **kwargs)
                    logger.write_log(
                        date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        module_name=func.__module__,
                        user_name=data.get("username"),
                        user_rights=data.get("rights"),
                        function_name=func.__name__,
                        function_description=re.sub(r'\s+', ' ', str(func.__doc__).replace('\n', '')).replace(' ', '',
                                                                                                              1),
                        function_result_type=str(type(result)),
                        message=data.get(result[-1])[0],
                    )
                    return result
                except Exception as e:
                    print(Exception)
                    logger.write_log(
                        date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        module_name=func.__module__,
                        user_name=data.get("username"),
                        user_rights=data.get("rights"),
                        function_name=func.__name__,
                        function_description=re.sub(r'\s+', ' ', str(func.__doc__).replace('\n', '')).replace(' ', '',
                                                                                                              1),
                        function_result_type="None",
                        message="Необработанная ошибка сервера",
                        traceback=str(traceback.format_exc(tracing_depth))
                    )

            return build_log_wrapper

        return build_log
