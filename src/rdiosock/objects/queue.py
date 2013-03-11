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

    def parse_track_keys(self, key, value):
        track_keys = []
        for item in value:
            track_keys.append(item['key'])
        self.track_keys = track_keys
