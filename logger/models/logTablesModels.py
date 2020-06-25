"""
Модуль, инициализирующий модели таблиц логгера
"""

from sqlalchemy import Column, Integer, String
from logger.loggerSettings import *


class LogJournal(Base):
    """
    Модель таблицы журнала. В таблицу заносятся:
    дата, имя модуля, имя пользователя, права пльзователя, имя функции, описание функции,
    статус операции, id записи лога, соответсвубщие вызванной функции
    """

    __tablename__ = "LogJournal"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    date = Column('date', String, nullable=False)
    module_name = Column('module_name', String, nullable=False)
    user_name = Column('user_name', String, nullable=False)
    user_rights = Column('user_rights', String, nullable=False)
    function_name = Column('function_name', String, nullable=False)
    function_description = Column('function_description', String, nullable=False)
    status = Column('status', String, nullable=False)
    function_result = Column('function_result', String, nullable=False)
    message = Column('message', String, nullable=False)
    traceback = Column('traceback', String, nullable=False)


Base.metadata.create_all(engine)
metadata = Base.metadata
