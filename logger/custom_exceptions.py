import werkzeug
from werkzeug.exceptions import HTTPException


class InsufficientStorage(werkzeug.exceptions.HTTPException):
    code = 507
    description = 'Not enough storage space.'


class SomeException(werkzeug.exceptions.HTTPException):
    code = 5000
    description = 'test HTTPexception'


class MyException(Exception):
    code = 10000
    description = 'my exception'

class MyCustomException(MyException):
    code = 10000
    description = 'my 1 custom exception!'
