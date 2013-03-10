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


import json
from rdiosock import Logr
from rdiosock.utils import camel_to_score


class RdioBaseItem(object):
    PARSE_NAME_MAP = {}
    PARSE_NAME_IGNORE = []
    PARSE_VALUE_METHODS = {}

    def __init__(self):
        if self._is_initialized('RdioBaseItem'):
            return

        self.__initialized = True

    def _is_initialized(self, name):
        return hasattr(self, '_' + name + '__initialized') and self.__initialized

    @classmethod
    def parse(cls, data):
        """Parse data into object

        @param data: Data to parse
        @type data: str or dict

        @rtype: RdioBaseItem
        """
        if data is None:
            return None

        if isinstance(data, str):
            data = json.loads(data)

        if type(data) is not dict:
            print type(data)
            raise ValueError()

        instance = cls()

        for key, value in data.items():
            score_key = camel_to_score(key)
            if score_key in cls.PARSE_NAME_MAP:
                score_key = cls.PARSE_NAME_MAP[score_key]

            if score_key in cls.PARSE_NAME_IGNORE:
                continue  # Skip this key

            if hasattr(instance, score_key):
                if score_key in cls.PARSE_VALUE_METHODS:
                    value = getattr(cls, cls.PARSE_VALUE_METHODS[score_key])(value)
                setattr(instance, score_key, value)
            else:
                Logr.warning("Unable to store data, key: %s", score_key)

        return instance


class RdioDataItem(RdioBaseItem):
    def __init__(self):
        RdioBaseItem.__init__(self)

        if self._is_initialized('RdioDataItem'):
            return

        #: @type: str
        self.key = None
        #: @type: str
        self.type = None
        #: @type: str
        self.url = None

        self.__initialized = True


class RdioIconItem(RdioDataItem):
    def __init__(self):
        RdioDataItem.__init__(self)

        if self._is_initialized('RdioIconItem'):
            return

        #: @type: str
        self.icon = None
        #: @type: str
        self.base_icon = None

        self.__initialized = True


class RdioNamedItem(RdioDataItem):
    def __init__(self):
        RdioDataItem.__init__(self)

        if self._is_initialized('RdioNamedItem'):
            return

        #: @type: str
        self.name = None
        #: @type: str
        self.short_url = None
        #: @type: int
        self.length = None

        self.__initialized = True


class RdioMediaItem(RdioNamedItem, RdioIconItem):
    def __init__(self):
        RdioNamedItem.__init__(self)
        RdioIconItem.__init__(self)

        if self._is_initialized('RdioMediaItem'):
            return

        #: @type: str
        self.album_key = None
        #: @type: str
        self.album_url = None

        #: @type: str
        self.artist = None
        #: @type: str
        self.artist_key = None
        #: @type: str
        self.artist_url = None

        #: @type: bool
        self.can_sample = None
        #: @type: bool
        self.can_stream = None
        #: @type: bool
        self.can_tether = None
        #: @type: bool
        self.is_clean = None
        #: @type: bool
        self.is_explicit = None

        #: @type: int
        self.duration = None

        # TODO: Unknown type, float?
        self.price = None

        #: @type: str
        self.embed_url = None
        #: @type: str
        self.iframe_url = None

        self.__initialized = True
