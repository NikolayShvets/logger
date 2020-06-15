# -*- coding: utf-8 -*-
"""аттрибут __doc__ python
Модуль логгирования. Создает логгер - декоратор, записывающий лог
в локальную базу данных <sqlite>
"""
import logging
import logging.config
import os
import sys
import sqlite3
from functools import wraps
from datetime import datetime
class Logger:
    """
    Класс Logger - декоратор, оборачивающий вызываемые пользователем функции,
    добавляя функционал логгирования действий переданного пользователя.
    """
    def __init__(self, username: str, rights: str):
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
        self.conn = sqlite3.connect("logJournal.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __call__(self, func):
        """
        Оператор вызова декоратора.
        :param func: оборачиваемя функция
        :return: обёртка над оборачиваемой функцией
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обертка над переданной функцией func.
            :param args: спиоск неименованных аргументов.
            :param kwargs: словарь именованных аргументов.
            :return: результат работы оборачиваемой функции func
            """

            try:
                res = func(*args, **kwargs)
                log_record = [
                    (
                        "DEBUG",
                        "SUCCESS " + str(res),
                        "some info",
                        "OK"
                    )
                ]
                self.cursor.executemany(
                    "INSERT INTO DebugLog \
                        (status, function_result, message, traceback) \
                        VALUES (?,?,?,?)",
                    log_record
                )
                self.conn.commit()
                log_record = [
                    (
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        self.simplexLogger.name,
                        func.__module__,
                        self.username,
                        self.rights,
                        func.__name__,
                        func.__doc__,
                        str(self.cursor.lastrowid)
                    )
                ]
                self.cursor.executemany(
                    "INSERT INTO Journal \
                            (date, logger_name, module_name, user_name, user_rights, \
                            function_name, function_description, log) \
                            VALUES (?,?,?,?,?,?,?,?)",
                    log_record)
                self.conn.commit()
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
                self.cursor.executemany(
                    "INSERT INTO DebugLog \
                        (status, function_result, message, traceback) \
                        VALUES (?,?,?,?)",
                    log_record
                )
                self.conn.commit()
                log_record = [
                    (
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        self.simplexLogger.name,
                        func.__module__,
                        self.username,
                        self.rights,
                        func.__name__,
                        func.__doc__,
                        str(self.cursor.lastrowid)
                    )
                ]
                self.cursor.executemany(
                    "INSERT INTO Journal \
                            (date, logger_name, module_name, user_name, user_rights, \
                            function_name, function_description, log) \
                            VALUES (?,?,?,?,?,?,?,?)",
                    log_record)
                self.conn.commit()
        return wrapper


