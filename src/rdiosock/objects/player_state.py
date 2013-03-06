from rdiosock.objects.source import RdioSource
from rdiosock.objects.base import RdioBaseItem


class RdioPlayerState(RdioBaseItem):
    def __init__(self):
        RdioBaseItem.__init__(self)

        #: @type: RdioSource
        self.current_source = None

        #: @type: int
        self.repeat = None
        #: @type: bool
        self.shuffle = None
        # TODO: Type Unknown
        self.station = None

        #: @type: int
        self.version = None

    def __setattr__(self, name, value):
        if name == 'current_source':
            value = RdioSource.parse(value)

        super(RdioPlayerState, self).__setattr__(name, value)

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioPlayerState
        """
        return super(RdioPlayerState, cls).parse(data)
