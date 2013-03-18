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
from rdiosock.services import RdioService
from rdiosock.utils import EventHook


class RdioPrivateService(RdioService):
    """Private service manager"""
    __topic__ = 'private'

    def __init__(self, sock):
        self.on_player_state_changed = EventHook()
        self.on_queue_changed = EventHook()

        super(RdioPrivateService, self).__init__(sock)

    def received_message(self, message):
        Logr.debug("received_message: %s", message.data['event'])

        if message.data['event'] == 'playerStateChanged':
            Logr.debug("on_player_state_changed")
            self.on_player_state_changed()
        elif message.data['event'] == 'queueChanged':
            Logr.debug("on_queue_changed")
            self.on_queue_changed()
        else:
            Logr.warning("Unhandled message received: %s", message.data['event'])

    def publish_command(self, event, command_type, **kwargs):
        data = {
            'command': {
                'type': command_type
            }
        }

        for key, value in kwargs.items():
            data['command'][key] = value

        self.publish_event(event, data)
