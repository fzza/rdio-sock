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


import os
import sys
from console import login


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(current_dir + "\\..\\"))
from rdiosock import RdioSock, Logr


def player_state_changed(player_state):
    Logr.info("player_state_changed")

    current_position = player_state['currentSource']['currentPosition']
    Logr.info("current_position = %s", current_position)

    current_track = player_state['currentSource']['tracks']['items'][current_position]

    print "%s - %s - %s" % (current_track['name'], current_track['album'], current_track['artist'])


if __name__ == '__main__':
    print "Connecting..."
    rdio = RdioSock()
    login(rdio)

    # Connected Callback
    def pubsub_connected():
        print "Connected"
        # Bind player events
        rdio.player.bind(player_state_changed, 'player_state')

        rdio.player.update()

    rdio.pubsub.on_connected.bind(pubsub_connected)

    rdio.pubsub.connect()

    while True:
        if raw_input() == 'exit':
            break
