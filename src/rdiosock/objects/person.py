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
