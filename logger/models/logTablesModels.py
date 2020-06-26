"""
Модуль, инициализирующий модели таблиц логгера
"""

from sqlalchemy import Column, Integer, String
from logger.loggerSettings import *
from datetime import datetime


class LogJournal(Base):
    """
    Модель таблицы журнала. В таблицу заносятся:
    дата, имя модуля, имя пользователя, права пльзователя, имя функции, описание функции,
    статус операции, id записи лога, соответсвубщие вызванной функции
    """

    __tablename__ = "LogJournal"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    date = Column('date', String, default=datetime.now())
    module_name = Column('module_name', String, nullable=False)
    user_name = Column('user_name', String, nullable=True)
    user_rights = Column('user_rights', String, nullable=True)
    function_name = Column('function_name', String, nullable=False)
    function_description = Column('function_description', String, nullable=True)
    function_result_type = Column('function_result_type', String, nullable=True)
    message = Column('message', String, default="Код не обработан")
    traceback = Column('traceback', String, nullable=True)


Base.metadata.create_all(engine)
metadata = Base.metadata
