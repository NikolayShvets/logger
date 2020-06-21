# -*- coding: utf-8 -*-
"""аттрибут __doc__ python
Модуль логгирования. Создает логгер - декоратор, записывающий лог
в локальную базу данных <sqlite>
"""

import traceback
from logger import loggerThread
from functools import wraps
from logger.models.logTablesModels import Journal, DebugLog, engine, Session
from datetime import datetime
import threading


class logger:
    """
    Класс Logger - декоратор, оборачивающий вызываемые пользователем функции,
    добавляя функционал логгирования действий переданного пользователя.
    """

    def __init__(self, user_name: str, user_rights: str, code_only: bool = False):
        """
        Конструктор функтора Logger. Инициализирует и агрегирует объект класса <logging>,
        настраивая его в соответсвии с файлом конфигурации  <LoggerConfig.conf>.
        Инициализирует жуернал лога, как объект базы данных <sqlite>.
        :param username: Имя пользователя
        :param rights: Права доступа пользователя
        """

        self.code_only = code_only
        self.user_name = user_name
        self.user_rights = user_rights


    @loggerThread.logger_thread
    def __write_log__(self, table_name: str, **kwargs):
        DBSession = Session(bind=engine)
        if table_name == "DebugLog":
            DBSession.add(DebugLog(**kwargs))
        elif table_name == "Journal":
            DBSession.add(Journal(**kwargs))
        DBSession.commit()

    def __call__(self, func):
        """
        Оператор вызова декоратора.
        :param func: оборачиваемя функция
        :return: обёртка над оборачиваемой функцией
        """

        @wraps(func)
        def wrapper(*args: tuple, **kwargs: list):
            """
            Обертка над переданной функцией func.
            :param args: кортеж неименованных аргументов.
            :param kwargs: список именованных аргументов.
            :return: результат работы оборачиваемой функции func
            """

            try:
                log_res = res = func(*args, **kwargs)
                if self.code_only:
                    log_res = res[1]
                self.__write_log__("DebugLog",
                                   function_result="SUCCESS " + str(log_res),
                                   message="Without any errors",
                                   traceback=str(traceback.format_exc(2))
                                   )
                self.__write_log__("Journal",
                                   date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   module_name=func.__module__,
                                   user_name=self.user_name,
                                   user_rights=self.user_rights,
                                   function_name=func.__name__,
                                   function_description=func.__doc__,
                                   status="OK",
                                   log_id=0
                                   )
                return res
            except Exception as e:
                self.__write_log__("DebugLog",
                                   function_result="FAILRUE",
                                   message="Without any errors",
                                   traceback=str(traceback.format_exc(2))
                                   )
                self.__write_log__("Journal",
                                   date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   module_name=func.__module__,
                                   user_name=self.user_name,
                                   user_rights=self.user_rights,
                                   function_name=func.__name__,
                                   function_description=func.__doc__,
                                   status="OK",
                                   log_id=0
                                   )

        return wrapper
