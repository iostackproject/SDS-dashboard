from horizon import exceptions


class ZoeException(exceptions.HorizonException):
    def __init__(self, message):
        super(ZoeException, self).__init__(message)