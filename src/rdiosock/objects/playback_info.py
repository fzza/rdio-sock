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


from rdiosock.objects import RdioTrack


class RdioPlaybackInfo(RdioTrack):
    """Rdio Playback Info"""

    def __init__(self):
        RdioTrack.__init__(self)

        #: :type: bool
        self.mp4 = None

        #: :type: int
        self.shost = None

        #: :type: str
        self.surl = None

        #: :type: str
        self.stream_app = None

        #: :type: str
        self.stream_host = None

        #: :type: bool
        self.user_has_unlimited = None

    @classmethod
    def parse(cls, data):
        """Parse data into RdioPlaybackInfo object

        :param data: Data to parse
        :type data: str or dict

        :rtype: :class:`rdiosock.objects.playback_info.RdioPlaybackInfo`
        """
        return super(RdioPlaybackInfo, cls).parse(data)
