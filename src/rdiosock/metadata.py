from pprint import pprint


class SEARCH_TYPES:
    NONE        = 0
    ARTIST      = 1
    ALBUM       = 2
    TRACK       = 4
    PLAYLIST    = 8
    USER        = 16
    LABEL       = 32

    ALL         = (
        ARTIST |
        ALBUM |
        TRACK |
        PLAYLIST |
        USER |
        LABEL
    )

    _MAP = {
        ARTIST:     'Artist',
        ALBUM:      'Album',
        TRACK:      'Track',
        PLAYLIST:   'Playlist',
        USER:       'User',
        LABEL:      'Label'
    }

    @classmethod
    def parse(cls, value):
        if type(value) is int:
            value = cls._parse_bit(value)

        items = []
        for key in value:
            items.append(cls._MAP[key])

        return items

    @classmethod
    def _parse_bit(cls, value):
        items = []

        for key in cls._MAP:
            if (value & key) == key:
                items.append(key)

        return items


class SEARCH_EXTRAS:
    NONE            = 0
    LOCATION        = 1
    USERNAME        = 2
    STATIONS        = 4
    DESCRIPTION     = 8

    FOLLOWER_COUNT  = 16
    FOLLOWING_COUNT = 32
    FAVORITE_COUNT  = 64
    SET_COUNT       = 128

    ICON_250x375    = 256
    ICON_500x750    = 512
    ICON_250x333    = 1024
    ICON_500x667    = 2048

    ALL             = (
        LOCATION |
        USERNAME |
        STATIONS |
        DESCRIPTION |
        FOLLOWER_COUNT |
        FOLLOWING_COUNT |
        FAVORITE_COUNT |
        SET_COUNT |
        ICON_250x375 |
        ICON_500x750 |
        ICON_250x333 |
        ICON_500x667
    )

    _MAP = {
        LOCATION: 'location',
        USERNAME: 'username',
        STATIONS: 'stations',
        DESCRIPTION: 'description',

        FOLLOWER_COUNT: 'followerCount',
        FOLLOWING_COUNT: 'followingCount',
        FAVORITE_COUNT: 'favoriteCount',
        SET_COUNT: 'setCount',

        ICON_250x375: 'icon250x375',
        ICON_500x750: 'icon500x750',
        ICON_250x333: 'icon250x333',
        ICON_500x667: 'icon500x667'
    }

    @classmethod
    def parse(cls, value):
        if type(value) is int:
            value = cls._parse_bit(value)

        items = []
        for key in value:
            items.append(cls._MAP[key])

        return items

    @classmethod
    def _parse_bit(cls, value):
        items = []

        for key in cls._MAP:
            if (value & key) == key:
                items.append(key)

        return items


class RdioMetadata(object):
    def __init__(self, sock):
        """
        @type sock: RdioSock
        """
        self._sock = sock

    def search(self, query, search_type=SEARCH_TYPES.ALL, extras=SEARCH_EXTRAS.ALL):
        """Search for media item.

        @param query: Search query
        @type query: str
        """

        search_type = SEARCH_TYPES.parse(search_type)
        extras = SEARCH_EXTRAS.parse(extras)

        print search_type
        print extras

        result = self._sock._api_post('search', {
            'query': query,
            'types[]': search_type
        }, secure=False, extras=extras)

        pprint(result)
