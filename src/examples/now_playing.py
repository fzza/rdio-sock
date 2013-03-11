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


def last_song_played_changed(last_song_played):
    """
    @type last_song_played: RdioTrack
    """
    print "%s - %s - %s" % (last_song_played.name,
                            last_song_played.album,
                            last_song_played.artist)


if __name__ == '__main__':
    print "Connecting..."
    rdio = RdioSock()
    login(rdio)

    # Connected Callback
    def pubsub_connected():
        print "Connected"
        # Subscribe services into pubsub updates
        rdio.pubsub.subscribe(rdio.services.fields)

        # Get notified when song changes (when 'last_song_played' field changes)
        rdio.player.bind(last_song_played_changed, 'last_song_played')

        rdio.player.update()  # Get latest player_state

        # Get currently playing song from player_state
        last_song_played_changed(rdio.player.player_state.current_source.tracks[
            rdio.player.player_state.current_source.current_position
        ])

    rdio.pubsub.on_connected.bind(pubsub_connected)

    rdio.pubsub.connect()

    while True:
        if raw_input() == 'exit':
            break
