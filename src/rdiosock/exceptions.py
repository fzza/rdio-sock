from pprint import pprint


class RdioException(BaseException):
    def __init__(self, result=None):
        if result is not None and result['status'] != 'error':
            pprint(result)
            raise ValueError()

        if result is None:
            result = {}

        self.code = int(result.get('code', -1))
        self.message=result.get('message', "")

        super(RdioException, self).__init__()

    def __str__(self):
        return '(%s) "%s"' % (self.code, self.message)
