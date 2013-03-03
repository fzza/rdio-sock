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


# Pattern used for pulling environment information from a web page
PATTERN_ENV = r'Env\s*=\s*\{\s*'\
              r'VERSION\s*:\s*(?P<version>\{.*?\})\s*,\s*'\
              r'currentUser\s*:\s*(?P<currentUser>\{.*?\})\s*,\s*'\
              r'serverInfo\s*:\s*(?P<serverInfo>\{.*?\})\s*\};'

PATTERN_CAMEL2SCORE_FIRST = r'(.)([A-Z][a-z]+)'
PATTERN_CAMEL2SCORE_ALL = r'([a-z0-9])([A-Z])'

URL_BASE = 'www.rdio.com'