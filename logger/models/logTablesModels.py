"""
Модуль, инициализирующий модели таблиц логгера
"""

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker()

class Journal(Base):
    """
    Модель таблицы журнала. В таблицу заносятся:
    дата, имя модуля, имя пользователя, права пльзователя, имя функции, описание функции,
    статус операции, id записи лога, соответсвубщие вызванной функции
    """

    __tablename__ = "Journal"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    date = Column('date', String, nullable=False)
    module_name = Column('module_name', String, nullable=False)
    user_name = Column('user_name', String, nullable=False)
    user_rights = Column('user_rights', String, nullable=False)
    function_name = Column('function_name', String, nullable=False)
    function_description = Column('function_description', String, nullable=False)
    status = Column('status', String, nullable=False)
    log_id = Column(Integer, ForeignKey("DebugLog.id"))


class DebugLog(Base):
    """
    Модель таблицы журнала. В таблицу заносятся:
    результат функции, сообщение, трассировщик ошибки, соответсвующие
    вызванной функци
    """

    __tablename__ = "DebugLog"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    function_result = Column('function_result', String, nullable=False)
    message = Column('message', String, nullable=False)
    traceback = Column('traceback', String, nullable=False)


Base.metadata.create_all(engine)
metadata = Base.metadata
