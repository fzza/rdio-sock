# rdio-sock - Rdio WebSocket Library
# Copyright (C) 2013  fzza- <fzzzzzzzza@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from rdiosock import Logr
from rdiosock.objects.album import RdioAlbum
from rdiosock.objects.track import RdioTrack
from rdiosock.objects.base import RdioMediaItem


class RdioSource(RdioMediaItem):
    def __init__(self):
        RdioMediaItem.__init__(self)

    @staticmethod
    def parse_source(value):
        if value is None:
            return None

        if value.get('type') == 't':
            return RdioTrackSource.parse(value)
        elif value.get('type') == 'al':
            return RdioAlbumSource.parse(value)

        Logr.warning("'%s' source type not implemented", value.get('type'))
        return None

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioSource
        """

        return super(RdioSource, cls).parse(data)


class RdioTrackSource(RdioTrack, RdioSource):
    def __init__(self):
        RdioTrack.__init__(self)
        RdioSource.__init__(self)

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioTrackSource
        """
        return super(RdioTrackSource, cls).parse(data)


class RdioAlbumSource(RdioAlbum, RdioSource):
    def __init__(self):
        RdioAlbum.__init__(self)
        RdioSource.__init__(self)

        #: @type: str
        self.album_key = None
        #: @type: str
        self.album_url = None

        #: @type: int
        self.current_position = None

        #: @type: str
        self.raw_artist_key = None

        #: @type: str
        self.user_key = None
        #: @type: str
        self.user_name = None

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioAlbumSource
        """
        return super(RdioAlbumSource, cls).parse(data)
