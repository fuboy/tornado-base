# singleton pattern
class Constants(object):

    _instance = None

    MESSAGE_TYPE_INFO = 'info'
    MESSAGE_TYPE_SUCCESS = 'success'
    MESSAGE_TYPE_ERROR = 'error'
    MESSAGE_TYPE_EXCEPTION = 'exception'

    MESSAGE_TYPES = [MESSAGE_TYPE_ERROR, MESSAGE_TYPE_EXCEPTION, MESSAGE_TYPE_INFO, MESSAGE_TYPE_SUCCESS]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Constants, cls).__new__(cls, *args, **kwargs)

        return cls._instance