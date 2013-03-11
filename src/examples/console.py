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


import code
import logging
import os
from pprint import pprint
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(current_dir + "\\..\\"))

from rdiosock import RdioSock
from rdiosock.exceptions import RdioException
from rdiosock.logr import Logr


def login(rdio):
    username = None
    password = None

    # Read auth from /console.auth
    auth_path = current_dir + "/auth"
    if os.path.exists(auth_path):
        fp = open(auth_path)
        data = fp.read()
        fp.close()
        username, password = data.split(':')

    # Username console input
    if username is None:
        username = raw_input('Username: ')

    # Password console input
    if password is None:
        password = raw_input('Password: ')

    # Login to Rdio
    try:
        rdio.user.login(username, password)
    except RdioException, e:
        Logr.warning('failed to login, unable to continue')
        raise


def last_song_played_changed(last_song_played):
    """
    @type last_song_played: RdioTrack
    """
    Logr.info("%s - %s - %s",
              last_song_played.name,
              last_song_played.album,
              last_song_played.artist)


def queue_changed(queue):
    """
    @type queue: RdioQueue
    """
    Logr.info("%s", queue.track_keys)

if __name__ == '__main__':
    Logr.configure(logging.DEBUG)
    rdio = RdioSock()
    login(rdio)

    # Connected callback
    def pubsub_connected():
        Logr.info("pubsub_connected")
        # Subscribe services into pubsub updates
        rdio.pubsub.subscribe(rdio.services.fields)
        rdio.pubsub.subscribe(rdio.services.private)

        # Bind player events
        rdio.player.bind(last_song_played_changed, 'last_song_played')
        rdio.player.bind(queue_changed, 'queue')

        rdio.player.update()

        # Get currently playing song from player_state
        last_song_played_changed(rdio.player.player_state.current_source.tracks[
            rdio.player.player_state.current_source.current_position
        ])

    rdio.pubsub.on_connected.bind(pubsub_connected)

    rdio.pubsub.connect()

    code.interact(local=globals())
