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


class RdioException(BaseException):
    pass


class RdioNetworkError(RdioException):
    def __init__(self, message, code=-1):
        self.message = message
        self.code = code

        super(RdioNetworkError, self).__init__()

    def __str__(self):
        return '(%s) "%s"' % (self.code, self.message)


class RdioApiError(RdioException):
    def __init__(self, result=None):
        if result is None:
            result = {}

        self.message = result.get('message', '')
        self.code = result.get('code', -1)

        super(RdioApiError, self).__init__()

    def __str__(self):
        return '(%s) "%s"' % (self.code, self.message)
