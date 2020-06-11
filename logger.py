"""
Модуль с настраиваемым логгером. Лог состоит из двух частей:
первая часть - Body, в формате (YYYY:MM:DD:HH:MM:SS MODULE NAME - LEVEL:).
Вторая часть - Message, в формате (USER_RIGHTS|USER_NAME|USER_ACTION|ACTION_RESULT_CODE|).
"""

import logging
import logging.config
from datetime import datetime

def textFileDecorator(func):#==> class 'function'
    """
    Декоратор базового метода  getBodyLog (получение первой части лога - тела).
    :param func: оборачиваемая функция getBodyLog.
    :return: wrapper - обертка функции getBodyLog, добавляющая возможность.
    вывода лога в текстовый файл.
    """
    def wrapper(self, level, user, action, actionCode):#==> class 'str'
        """
        Обертка функции getBodyLog. Конкатенирует вывод функции getBodyLog и messege,
        где message - вторая часть лога, см. выше.
        :param level: уровнь важности лога. Причем DEBUG < INFO < WARNING < ERROR < CRITICAL.
        :param user: объект, содержащий информаицю о пользователе. (права доступа, имя).
        :param action: объект, содержащий информацию о совершенном действии.
        :param actionCode: объект, отражающий стаус действия.
        :return: полная строка лога, содержащая обе его части.
        """
        body = func(self, level)
        message = str(user["rights"]) + "|" + str(user["name"]) + "|" + str(action) + "|" + str(actionCode)
        return body + message
    return wrapper

def xmlFileDecorator(func):#==> class 'function'
    """
    Декоратор базового метода  getBodyLog (получение первой части лога - тела).
    :param func: оборачиваемая функция getBodyLog.
    :return: wrapper - обертка функции getBodyLog, добавляющая возможность вывода лога в текстовый файл.
    """
    def wrapper(self, level, user, adtion, actionCode):#==> class 'str'
        """

        :param self:
        :param level:
        :param user:
        :param adtion:
        :param actionCode:
        :return:
        """
        pass
    return wrapper

class SimplexLogger:
    """
    Класс логерра.
    """
    def __init__(self, logFileName):
        """
        ( Конструктор. Агрегирует класс logging,
        указывая как имя логгера имя модуля, из которого он вызван.
        Параметры агрегированного класса настраиваются согласно
        содержимому файла конфигрурации "log.conf". ) -
        """
        #logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
        #self.logger = logging.getLogger(__name__)
        self.logFile = open(logFileName, "a")

    @textFileDecorator
    def getBodyLog(self, level): #==> class 'str'
        """
        Метод, собирающий тело лога. Далее будет декорироваться.
        :param level: уровнь важности лога. class 'str'.
        :return: возвращает строку, содержащую первую часть лога - body. class 'str'.
        """
        return str(self.getTime()) + " " + __name__ + " - " + level + ":"

    def addLog(self, newLog):
        """
        Метод, записывающий новый лог в журнал.
        :param newLog: полная строка лога (body + message) class 'str'.
        """
        self.logFile.write(newLog + "\n")

    def getTime(self):#==> class 'str'
        """
        Метод, возвращающий строку с текущей датой в формате ДЕНЬ МЕСЯЦ ГОД ЧАСЫ МИНУТЫ СЕКУНДЫ.
        :return: возвращает строку с датой. class 'str'.
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

sl = SimplexLogger("logFile.log")
user = {"rights":"user", "name":"Nikolay Shvets"}
action = "PUT"
actionCode = "500"
print(sl.getBodyLog("DEBUG", user, action, actionCode))
sl.addLog(sl.getBodyLog("ERROR", user, action, actionCode))