# -*- coding: utf-8 -*-
import logging
import logging.config
from datetime import datetime
import os
import sys
from functools import wraps
import sqlite3

class Logger:
    def __init__(self, username, rights):
        logging.config.fileConfig(fname="LoggerConfig.conf", disable_existing_loggers=False)
        self.simplexLogger = logging.getLogger("SimplexLogger")
        self.username = username
        self.rights = rights
        self.conn = sqlite3.connect("LOGDB.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        '''self.cursor.execute(
            """
            CREATE TABLE debug(
            date text NOT NULL,
            registrator_name text NOT NULL,
            module_name text NOT NULL,
            username text NOT NULL,
            rights text NOT NULL,
            funcname text NOT NULL,
            result text NOT NULL,
            message text NOT NULL
            )
            """
        )
        self.conn.commit()
        self.cursor.execute(
            """
            CREATE TABLE exceptions(
            date text NOT NULL,
            registrator_name text NOT NULL,
            module_name text NOT NULL,
            username text NOT NULL,
            rights text NOT NULL,
            funcname text NOT NULL,
            message text NOT NULL
            )
            """
        )
        self.conn.commit()'''

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                self.simplexLogger.info(f"User {self.username}({self.rights}) ==> {func.__name__}({args},{kwargs}) ==> {res}")
                logRecord = [
                    (
                        str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                        str(self.simplexLogger.name),
                        str(os.path.basename(sys.argv[0])),
                        str(self.username),
                        str(self.rights),
                        str(func.__name__),
                        str(res),
                        "DEBUG INFORMATION"
                     )
                ]
                self.cursor.executemany("INSERT INTO debug VALUES (?,?,?,?,?,?,?,?)", logRecord)
                self.conn.commit()
                return res
            except Exception as e:
                self.simplexLogger.exception("Exception")
                logRecord = [
                    (
                        str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                        str(self.simplexLogger.name),
                        str(os.path.basename(sys.argv[0])),
                        str(self.username),
                        str(self.rights),
                        str(func.__name__),
                        "ERROR INFORMATION"
                    )
                ]
                self.cursor.executemany("INSERT INTO exceptions VALUES (?,?,?,?,?,?,?)", logRecord)
                self.conn.commit()
        return wrapper


