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

from rdiosock.services import RdioService
from rdiosock.utils import EventHook


class RdioFieldService(RdioService):
    """Field service manager"""
    __topic__ = 'fields'

    def __init__(self, sock):
        self.fields = {}

        self.on_changed = EventHook()

        super(RdioFieldService, self).__init__(sock)

    def received_changed(self, fields):
        for field, value in fields.items():
            self.fields[field] = value
            self.on_changed[field](field, value)

    def received_message(self, message):
        if message.data['event'] == 'changed':
            if 'fields' not in message.data:
                Logr.warning('invalid message received')
            else:
                self.received_changed(message.data['fields'])
