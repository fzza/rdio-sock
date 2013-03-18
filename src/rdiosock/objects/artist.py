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


from rdiosock.objects.base import RdioNamedItem, RdioIconItem


class RdioArtist(RdioNamedItem, RdioIconItem):
    def __init__(self):
        RdioNamedItem.__init__(self)
        RdioIconItem.__init__(self)

        #: @type: int
        self.album_count = None

        # TODO: Unknown type
        self.band_members = None

        #: @type: str
        self.banner_alignment = None
        #: @type: str
        self.banner_background_color = None
        #: @type: str
        self.cover_photo_url = None

        #: @type: bool
        self.has_icon = None
        #: @type: bool
        self.has_influenced_artists = None
        #: @type: bool
        self.has_influential_artists = None
        #: @type: bool
        self.has_radio = None
        #: @type: bool
        self.has_related_artists = None
        #: @type: bool
        self.has_review = None

        #: @type: bool
        self.in_program = None

        #: @type: list
        self.stations = None

        #: @type: str
        self.top_album_icon = None
        #: @type: str
        self.top_songs_key = None

        #: @type: str
        self.radio_key = None

        #: @type: int
        self.play_count = None

    @classmethod
    def parse(cls, data):
        """Parse data dictionary into RdioArtist object

        :param data: Data to parse
        :type data: str or dict

        :rtype: :class:`rdiosock.objects.artist.RdioArtist`
        """
        return super(RdioArtist, cls).parse(data)
