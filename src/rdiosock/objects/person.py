from rdiosock.objects.base import RdioIconItem


class RdioPerson(RdioIconItem):
    def __init__(self):
        RdioIconItem.__init__(self)

        #: @type: str
        self.first_name = None
        #: @type: str
        self.last_name = None
        #: @type: str
        self.gender = None
        #: @type: str
        self.location = None

        #: @type: bool
        self.can_unfollow = None
        #: @type: bool
        self.is_protected = None

        # TODO: Type Unknown, str?
        self.follower_state = None
        #: @type: str
        self.following_state = None

        #: @type: int
        self.library_version = None

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioPerson
        """
        return super(RdioPerson, cls).parse(data)
