class RdioException(BaseException):
    pass


class RdioNetworkError(RdioException):
    def __init__(self, message, code=-1):
        self.message = message
        self.code = code

        super(RdioNetworkError, self).__init__()

    def __str__(self):
        return '(%s) "%s"' % (self.code, self.message)


class RdioApiError(RdioException):
    def __init__(self, result=None):
        if result is None:
            result = {}

        self.message = result.get('message', '')
        self.code = result.get('code', -1)

        super(RdioApiError, self).__init__()

    def __str__(self):
        return '(%s) "%s"' % (self.code, self.message)