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
