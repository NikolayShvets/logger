import threading
import sys


def logger_thread(func):
    """
    Декоратор, помещающий переданную функцию в новый поток
    :param func: переданная функция
    :return: декорированная функция func
    """

    def logger_thread_wrapper(*args: tuple, **kwargs: list):
        """
        Создает новый поток и помещает туда переданную функцию
        :param args: кортеж неименованных аргументов
        :param kwargs: список именованных аргументов
        :return: обертка над функцией func
        """
        current_thread = threading.Thread(target=func, args=args, kwargs=kwargs, name="logger_db_thread")
        current_thread.start()

    return logger_thread_wrapper
