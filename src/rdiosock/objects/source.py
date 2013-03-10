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


from rdiosock.objects.track import RdioTrack
from rdiosock.objects.base import RdioMediaItem


class RdioSource(RdioMediaItem):
    PARSE_NAME_MAP = {
        'icon400': 'icon_400'
    }
    PARSE_NAME_IGNORE = [
        'item_track_keys'
    ]
    PARSE_VALUE_METHODS = {
        'tracks': 'parse_tracks'
    }

    def __init__(self):
        RdioMediaItem.__init__(self)

        #: @type: list of str
        self.track_keys = None
        #: @type: list of RdioTrack
        self.tracks = None
        #: @type: int
        self.current_position = None

        # TODO: Parse dates
        #: @type: str
        self.display_date = None
        #: @type: str
        self.release_date = None

        #: @type: str
        self.icon_400 = None

        #: @type: str
        self.raw_artist_key = None

        #: @type: list or RdioPerson
        self.network_consumers = None

        #: @type: str
        self.user_key = None
        #: @type: str
        self.user_name = None

    @staticmethod
    def parse_tracks(value):
        """Parse tracks list dictionary

        @param value: tracks list dictionary
        @type value: dict
        """
        if not isinstance(value, dict):
            raise ValueError()

        if 'items' not in value:
            raise ValueError()

        if value.get('type') != 'list':
            raise ValueError()

        return_value = []

        for track in value.get('items', []):
            return_value.append(RdioTrack.parse(track))

        return return_value

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioSource
        """
        return super(RdioSource, cls).parse(data)
