from rdiosock.exceptions import RdioApiError
from rdiosock.objects.collection import RdioList


class SEARCH_TYPES:
    """Metadata search types"""
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
    """Metadata search extras"""
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
        :type sock: RdioSock
        """
        self._sock = sock

    def search(self, query, search_types=SEARCH_TYPES.ALL, search_extras=SEARCH_EXTRAS.ALL):
        """Search for media item.

        :param query: Search query
        :type query: str

        :param search_types: Search type (:class:`rdiosock.metadata.SEARCH_TYPES` bitwise-OR or list)
        :type search_types: int or list of int

        :param search_extras: Search result extras to include (:class:`rdiosock.metadata.SEARCH_EXTRAS` bitwise-OR or list)
        :type search_extras: int or list of int
        """

        result = self._sock._api_post('search', {
            'query': query,
            'types[]': SEARCH_TYPES.parse(search_types)
        }, secure=False, extras=SEARCH_EXTRAS.parse(search_extras))

        if result['status'] == 'error':
            raise RdioApiError(result)

        result = result['result']

        if result['type'] == 'list':
            return RdioList.parse(result)
        else:
            raise NotImplementedError()
