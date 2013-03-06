from rdiosock.objects.base import RdioBaseItem


class RdioQueue(RdioBaseItem):
    PARSE_NAME_MAP = {
        'data': 'track_keys'
    }
    PARSE_VALUE_METHODS = {
        'track_keys': 'parse_track_keys'
    }

    def __init__(self):
        RdioBaseItem.__init__(self)

        #: @type: list of str
        self.track_keys = None

        #: @type: int
        self.version = None

    @staticmethod
    def parse_track_keys(value):
        return_value = []
        for item in value:
            return_value.append(item['key'])
        return return_value
