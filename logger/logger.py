# -*- coding: utf-8 -*-
"""аттрибут __doc__ python
Модуль логгирования. Создает логгер - декоратор, записывающий лог
в базу данных, по указанному URI в файле настроек <config.py>
"""

import traceback
from logger import loggerThread
from functools import wraps
from logger.models.logTablesModels import LogJournal, engine, Session, tracing_depth
from datetime import datetime
import re


class logger:
    """
    Класс Logger - декоратор, оборачивающий вызываемые пользователем функции,
    добавляя функционал логгирования действий переданного пользователя.
    """

    def __init__(self, user_name: str = "None", user_rights: str = "None", code_only: bool = False) -> None:
        """

        :param username: Имя пользователя
        :param rights: Права доступа пользователя
        """
        """передавать пользовательскую сессиию"""
        self.code_only = code_only
        self.user_name = user_name
        self.user_rights = user_rights
        self.request_code = 500
        self.codes_description = {
            2: {
                200: "Запрос успешен.",
                201: "Запрос выполнен, новый ресурс создан.",
                202: "Запрос принят, но обработка не завершена.",
                203: "Информация в загловке получена из локальной или сторонней копии, а не от оригинального сервера.",
                204: "Код статуса и загловок переданы в ответе, но данный отсутствуют.",
                205: "Браузер должен очистить форму для этой транзакции для дополнительного ввода.",
                206: "Сервер возваращет часть данных."
            },
            4: {
                400: "Сервер не понял запрос.",
                401: "Запрашиваемая страница требует имя пользователя и пароль.",
                402: "На данный момент клиент не может использовать данный код.",
                403: "Доступ к запрашиваемой странице запрещен.",
                404: "Сервер не может найти запрашиваемую страницу.",
                405: "Метод, указанный в запросе, является недопустимым.",
                406: "Сервер генерирует ответ, который не может быть принят клиентом.",
                407: "Клиент должен авторизоваться с помощью прокси-сервера прежде чем запрос сможет быть обработан.",
                408: "Запрос длится дольше, чем сервер готов ждать.",
                409: "Запрос не может быть завершен из-за конфликта.",
                410: "Запрашиваемая страница больше недоступна.",
                411: "Элемент 'Content-Length' не определен. Сервер не может принять запрос без этого элемента.",
                412: "Сервер принял пред-условия запроса ошибочными.",
                413: "Сервер не примет данный запрос, так как тело запроса слишком большое.",
                414: "Сервер не примет данный запрос, так как URL слишком длинная.",
                415: "Сервер не примет данный запрос, так как данный тип медиафайла не поддерживается.",
                416: "Запрашиваемый диапазон байтов недоступен и находится за пределами диапазона.",
                417: "Ожидания, переданные в заголовке запроса не могут быть удовлетворены данным сервером."
            },
            5: {
                500: "Запрос не выполнен. Внутренняя ошибка сервера.",
                501: "Запрос не выполнен. Сервер не поддерживает запрашиваемый функционал.",
                502: "Запрос не выполнен. Сервер получил недоступный запрос от следующего сервера.",
                503: "Запрос не выполнен. На данный момент сервер перегружается или не работает.",
                504: "Соединение закрыто по времени.",
                505: "Сервер не поддерживает данную версию проткола HTTP."
            }
        }

    @loggerThread.logger_thread
    def __write_log__(self, **kwargs: list) -> None:
        """
        Метод, открывающий покдлючение к базе данных логера
        и записывающий в базу лог
        :param table_name: Имя таблицы, в которую осуществляется запись
        :param kwargs: list
        :return: None
        """

        DBSession = Session(bind=engine)
        DBSession.add(LogJournal(**kwargs))
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
                log_res = result = func(*args, **kwargs)
                self.request_code = result[-1]
                print(self.request_code)
                if self.code_only:
                    log_res = self.request_code
                self.__write_log__(
                    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    module_name=func.__module__,
                    user_name=self.user_name,
                    user_rights=self.user_rights,
                    function_name=func.__name__,
                    function_description=re.sub(r'\s+', ' ', str(func.__doc__).replace('\n', '')).replace(' ', '', 1),
                    status="SUCCESS",
                    function_result=str(log_res),
                    message=self.codes_description[self.request_code//100][self.request_code],
                    traceback=str(traceback.format_exc(tracing_depth))
                    )
                return result

            except Exception as e:
                print(self.request_code)
                self.__write_log__(
                    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    module_name=func.__module__,
                    user_name=self.user_name,
                    user_rights=self.user_rights,
                    function_name=func.__name__,
                    function_description=re.sub(r'\s+', ' ', str(func.__doc__).replace('\n', '')).replace(' ', '', 1),
                    status="ERROR",
                    function_result="None",
                    message=self.codes_description[self.request_code//100][self.request_code],
                    traceback=str(traceback.format_exc(tracing_depth))
                    )

        return wrapper
