from rdiosock.objects.base import RdioMediaItem


class RdioTrack(RdioMediaItem):
    def __init__(self):
        RdioMediaItem.__init__(self)

        #: @type: int
        self.track_num = None

        #: @type: str
        self.album = None
        #: @type: str
        self.album_artist = None
        #: @type: str
        self.album_artist_key = None

        #: @type: str
        self.radio_key = None

        #: @type: bool
        self.can_download = None
        #: @type: bool
        self.can_download_album_only = None

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioTrack
        """
        return super(RdioTrack, cls).parse(data)
