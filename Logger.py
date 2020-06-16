# -*- coding: utf-8 -*-
"""аттрибут __doc__ python
Модуль логгирования. Создает логгер - декоратор, записывающий лог
в локальную базу данных <sqlite>
"""
import logging
import logging.config
from loggerThread import *
import sqlite3
from functools import wraps
from datetime import datetime

@class_thread_decroator
class Logger:
    """
    Класс Logger - декоратор, оборачивающий вызываемые пользователем функции,
    добавляя функционал логгирования действий переданного пользователя.
    """
    def __init__(self, username: str, rights: str, code_only: bool = True):
        """
        Конструктор функтора Logger. Инициализирует и агрегирует объект класса <logging>,
        настраивая его в соответсвии с файлом конфигурации  <LoggerConfig.conf>.
        Инициализирует жуернал лога, как объект базы данных <sqlite>.
        :param username: Имя пользователя
        :param rights: Права доступа пользователя
        """
        logging.config.fileConfig(fname="LoggerConfig.conf", disable_existing_loggers=False)
        self.simplexLogger = logging.getLogger("SimplexLogger")
        self.username = username
        self.rights = rights
        self.code_only = code_only
        self.conn = sqlite3.connect("logJournal.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.debug_columns_names = ["status", "function_result", "message", "traceback"]

    #@logger_thread
    def __write_log__(self, values: list, table_name: str):
        """
        Записывает переданные значения в переданную таблицу базы данных.
        :param values: значения на запись в базу данных.
        :param table_name: имя таблицы, в которую производится запись.
        :return: None.
        """

        if table_name == "DebugLog":
            record = f"INSERT INTO {table_name} ("
            for column_name in self.debug_columns_names:
                record += column_name
                if self.debug_columns_names.index(column_name) != len(self.debug_columns_names) - 1:
                    record += ","
                else:
                    record += ") VALUES ("
                    for i in range(len(values[0]) - 1):
                        record += "?,"
                    record += "?)"
        else:
            record = f"INSERT INTO {table_name} VALUES ("
            for i in range(len(values[0]) - 1):
                record += "?,"
            record += "?)"
        print(record)
        self.cursor.executemany(record, values)
        self.conn.commit()

    def __call__(self, func):
        """
        Оператор вызова декоратора.
        :param func: оборачиваемя функция
        :return: обёртка над оборачиваемой функцией
        """
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict):
            """
            Обертка над переданной функцией func.
            :param args: кортеж неименованных аргументов.
            :param kwargs: список именованных аргументов.
            :return: результат работы оборачиваемой функции func
            """

            try:
                res = func(*args, **kwargs)
                log_record = [
                    (
                        "DEBUG",
                        "SUCCESS " + str(res),
                        "message",
                        "OK"
                    )
                ]
                self.__write_log__(log_record, "DebugLog",)
                self.cursor.execute("SELECT MAX(id) FROM DebugLog")
                log_record = [
                    (
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        func.__module__,
                        self.username,
                        self.rights,
                        func.__name__,
                        func.__doc__,
                        str(self.cursor.fetchall()[0])
                    )
                ]
                self.__write_log__(log_record, "Journal")
                self.simplexLogger.info(f"User {self.username}({self.rights}) ==> {func.__name__}({args},{kwargs}) ==> {res}")
                return res
            except Exception as e:
                self.simplexLogger.exception("Exception")
                log_record = [
                    (
                        "ERROR",
                        "FAILRUE",
                        "some info",
                        "Exception: "
                    )
                ]
                self.__write_log__(log_record, "DebugLog")
                self.cursor.execute("SELECT MAX(id) FROM DebugLog")
                log_record = [
                    (
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        func.__module__,
                        self.username,
                        self.rights,
                        func.__name__,
                        func.__doc__,
                        str(self.cursor.fetchall()[0])
                    )
                ]
                self.__write_log__(log_record, "Journal")
        return wrapper


