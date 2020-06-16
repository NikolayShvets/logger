import threading

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
        current_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        current_thread.start()
        return logger_thread_wrapper
def class_thread_decroator(cls):
    """
    Применяет декоратор logger_thread ко всем
    публичным методам переданного класса
    :param cls: переданный класс
    :return: декорированный класс cls
    """
    for name, method in iter(cls.__dict__.items()):
        if not name.startswith('_'):
            setattr(cls, name, logger_thread(method))
    return cls