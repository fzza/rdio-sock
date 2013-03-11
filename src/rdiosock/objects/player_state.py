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


from rdiosock.objects.source import RdioSource, RdioTrackSource, RdioAlbumSource
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
            value = RdioSource.parse_source(value)

        super(RdioPlayerState, self).__setattr__(name, value)

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioPlayerState
        """
        return super(RdioPlayerState, cls).parse(data)
