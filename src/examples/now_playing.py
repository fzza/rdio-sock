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
from rdiosock import RdioSock


def song_changed(track):
    """
    @type track: RdioTrack
    """
    print "%s - %s - %s" % (track.name, track.album, track.artist)


if __name__ == '__main__':
    print "Connecting..."
    rdio = RdioSock()
    login(rdio)

    # Connected Callback
    def pubsub_connected():
        print "Connected"
        # Subscribe services into pubsub updates
        rdio.pubsub.subscribe(rdio.services.fields)

        # Bind to 'on_song_changed' event
        rdio.player.on_song_changed.bind(song_changed)

        # Force a player update (will fire 'on_song_changed' with currently playing song)
        #
        # NOTE: Live song changes will automatically fire 'on_song_changed', so there
        # there should be no need to poll this method.
        rdio.player.update()

    rdio.pubsub.on_connected.bind(pubsub_connected)

    rdio.pubsub.connect()

    while True:
        if raw_input() == 'exit':
            break
