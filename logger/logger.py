# -*- coding: utf-8 -*-
"""
Модуль логгирования. Инициализирует статический класс логгера
с методом - декоратором, записывающим лог в базу данных, по указанному URI
в файле настроек <config.py>
"""

from logger import loggerThread
from logger.strlogger import str_logger, logger_dict
from functools import wraps
from logger.models.logTablesModels import LogJournal, Session, tracing_depth
from datetime import datetime
import traceback
from logger.custom_exceptions import *
from logger.recorder import recorder
import re


class Logger:
    @staticmethod
    @loggerThread.logger_thread
    def write_log(**kwargs) -> None:
        """
        Метод, открывающий покдлючение к базе данных логера и записывающий лог в базу данных
        :param kwargs: list
        :return: None
        """

        session = Session()
        try:
            session.add(LogJournal(**kwargs))
        except Exception as e:
            session.rollback()
            raise
        else:
            session.commit()

    @staticmethod
    def log(message: str, level: str = "DEBUG", exc_info: bool = False) -> None:
        """
        Метод для логгирования внутри оборачиваемых функций.

        :param exc_info: флаг исключения
        :param message: строка сообщения
        :param level: уровень сообщения
        :return: None
        """

        if not exc_info:
            if level in logger_dict.keys():
                logger_dict[level](message)
            else:
                logger_dict["DEBUG"](message)
        else:
            str_logger.exception(message)

    @staticmethod
    def change_uuid_try(func) -> None:
        """
        Функция, меняющая уникальный универсальный ключ в зависимости от наличия
        атрибута "__apidoc__" у функции-аргумента.
        :param func: функция
        :return: None
        """

        if hasattr(func, "__apidoc__"):
            recorder.change_uuid()

    @staticmethod
    def info_log(session: dict):
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

                # Собираем независимую от результата выполнения функции часть лога
                data = {}
                if session is not None:
                    data.update(dict(session))

                # Если фукнция имеет атрибут <__apidoc__> - это роут, ищем у него задокументированные HTTP коды
                if hasattr(func, "__apidoc__"):
                    data.update(func.__apidoc__.get("responses"))

                message = {
                    "date": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                    "module_name": func.__module__,
                    "user_name": data.get("username"),
                    "user_rights": data.get("rights"),
                    "function_name": func.__name__,
                    "function_description": re.sub(r"\s+", " ", str(func.__doc__).replace("\n", "")).replace(" ", "", 1)
                }
                try:
                    result = func(*args, **kwargs)

                    # Считаем, что код статуса запроса является последним элементом кортежа, возвращаемого из функции
                    if isinstance(result, tuple):
                        temp_msg = data.get(result[-1])
                        if temp_msg is not None:
                            temp_msg = temp_msg[0]
                        else:
                            temp_msg = "Код возврата не был задокументирован."
                    else:
                        temp_msg = "Функция не возвращает код HTTP статуса."

                    message.update(function_result_type=str(type(result)), index=recorder.get_uuid(),
                                   message=temp_msg)
                    Logger.write_log(**message)
                    Logger.change_uuid_try(func)
                    return result

                except Exception as e:

                    # Если поднятое исключение описано, забираем его описание
                    if isinstance(e, HTTPException) or isinstance(e, MyException):
                        message.update(message=e.description, index=recorder.get_uuid(),
                                       traceback=str(traceback.format_exc(tracing_depth)))
                        Logger.write_log(**message)
                        Logger.change_uuid_try(func)
                        return e, e.code

                    message.update(message="Необработанная ошибка сервера", index=recorder.get_uuid(),
                                   traceback=str(traceback.format_exc(tracing_depth)))
                    Logger.write_log(**message)
                    Logger.change_uuid_try(func)
                    return Exception

            return build_log_wrapper

        return build_log
