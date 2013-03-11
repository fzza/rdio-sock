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
from rdiosock.objects import DATA_TYPE_CLASSES
from rdiosock.objects.base import RdioBaseItem


class RdioCollection(RdioBaseItem):
    PARSE_VALUE_METHODS = {
        'person_count':     'parse_count',
        'track_count':      'parse_count',
        'album_count':      'parse_count',
        'playlist_count':   'parse_count',
        'label_count':      'parse_count',
        'artist_count':     'parse_count',
        'items':            'parse_items'
    }

    def __init__(self):
        RdioBaseItem.__init__(self)

        #: @type: int
        self.start = None
        #: @type: int
        self.total = None
        #: @type: int
        self.number_results = None
        #: @type: str
        self.type = None
        #: @type: dict
        self.type_count = None

        #: @type: list of RdioBaseItem
        self.items = None

    def __iter__(self):
        return self.items.__iter__()

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioCollection
        """
        return super(RdioCollection, cls).parse(data)

    def parse_items(self, key, value):
        pass

    def parse_count(self, key, value):
        if self.type_count is None:
            self.type_count = {}

        if not key.endswith("_count"):
            raise ValueError()

        self.type_count[key[:-6]] = value


class RdioList(RdioCollection):
    def __init__(self):
        RdioCollection.__init__(self)

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioList
        """
        return super(RdioCollection, cls).parse(data)

    def parse_items(self, key, value):
        items = []
        for item in value:
            if type(item) is not dict:
                raise ValueError()

            item_class = DATA_TYPE_CLASSES.get(item['type'])
            if item_class is not None:
                items.append(item_class.parse(item))
            else:
                Logr.warning("'%s' data type not implemented", item['type'])

        self.items = items
