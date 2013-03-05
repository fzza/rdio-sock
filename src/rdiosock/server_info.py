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


from rdiosock.logr import Logr
from rdiosock.utils import camel_to_score, update_attrs


class RdioServerInfo:
    def __init__(self, sock):
        self._sock = sock

        # Environment Information
        self.env_loaded = False

        self.country_code = None
        self.country_name = None
        self.locale = None

    def _load_env(self, serverInfo):
        Logr.debug('--------- ServerInfo ----------')
        update_attrs(self, serverInfo, trace=True)
