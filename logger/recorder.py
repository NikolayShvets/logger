import uuid


class Recorder:
    """
    Класс, реазлизующий логику индексирования
    внутри лога в рамках одного логгируемого роута
    """

    def __init__(self):
        """
        Конструктор класса. Устанавливает начальное значение
        уникального универсального индекса
        """

        self.index = str(uuid.uuid4())

    def get_uuid(self) -> str:
        """
        Функция, возвращающая уникальный универсальный индекс
        :return: строковое представление индекса, который хранится
                 как поле класса
        """

        return self.index

    def change_uuid(self) -> None:
        """
        Функция, изменяющая значение индекса
        :return: None
        """

        self.index = str(uuid.uuid4())


recorder = Recorder()
