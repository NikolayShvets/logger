from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://nikonikoni:niko1324@localhost:5432/Sberbank', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker()

class Journal(Base):
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

    def __init__(self, user_name, user_rights):
        self.user_name = user_name
        self.user_rights = user_rights

    def __repr__(self):
        return f"<User({self.user_name}, {self.user_rights})>"


class DebugLog(Base):
    __tablename__ = "DebugLog"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    function_result = Column('function_result', String, nullable=False)
    message = Column('message', String, nullable=False)
    traceback = Column('traceback', String, nullable=False)


Base.metadata.create_all(engine)
metadata = Base.metadata
