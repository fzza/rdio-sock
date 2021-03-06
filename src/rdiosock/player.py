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


import time
from rdiosock.exceptions import RdioApiError
from rdiosock.logr import Logr
from rdiosock.objects.playback_info import RdioPlaybackInfo
from rdiosock.objects.player_state import RdioPlayerState
from rdiosock.objects.queue import RdioQueue
from rdiosock.objects.source import RdioSource
from rdiosock.objects.track import RdioTrack
from rdiosock.utils import EventHook, camel_to_score


SONG_CHANGED_MIN_SECONDS = 8


class RdioPlayer(EventHook):
    REPEAT_ALL = 2
    REPEAT_ONE = 1
    REPEAT_NONE = 0

    def __init__(self, sock):
        """
        :type sock: RdioSock
        """
        super(RdioPlayer, self).__init__()
        self._sock = sock

        self.update_callback = None

        # Events
        self.on_song_changed = EventHook()
        self._on_song_changed_last_fire = None
        self._on_song_changed_last_value = None

        #: :type: RdioPlayerState
        self.player_state = None
        #: :type: RdioQueue
        self.queue = None

        #: :type: RdioTrack
        self.last_song_played = None
        # TODO: last_song_play_time
        self.last_song_play_time = None
        #: :type: RdioSource
        self.last_source_played = None

        # Bind field events
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSongPlayed')
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSourcePlayed')
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSongPlayTime')

        # Update 'player_state' or 'queue' if we receive a changed event
        self._sock.services.private.on_player_state_changed.bind(self.update)
        self._sock.services.private.on_queue_changed.bind(self.update)

    def _field_changed(self, name, value):
        name = camel_to_score(name)

        if hasattr(self, name):
            if name == 'last_song_played':
                value = RdioTrack.parse(value)
                self._fire_on_song_changed(value)
            elif name == 'last_source_played':
                value = RdioSource.parse_source(value)

            setattr(self, name, value)
            Logr.debug('_field_changed(%s) : updated', name)
        else:
            Logr.warning('_field_changed(%s) : not found', name)
        self[name](value)  # Fire event

    #
    # Fields
    #

    def set(self, key, value):
        self._sock.services.private.publish_command(
            'remote', 'set', key=key, value=value
        )

    # Volume
    def set_volume(self, level):
        self.set('volume', level)
    volume = property(None, set_volume)

    # Shuffle
    def set_shuffle(self, enabled):
        self.set('shuffle', enabled)
    shuffle = property(None, set_shuffle)

    # Repeat`
    def set_repeat(self, repeat_type):
        if repeat_type not in [RdioPlayer.REPEAT_ALL,
                               RdioPlayer.REPEAT_ONE,
                               RdioPlayer.REPEAT_NONE]:
            raise ValueError()

        self.set('repeat', repeat_type)
    repeat = property(None, set_repeat)

    # Position
    def set_position(self, position):
        self.set('position', position)
    position = property(None, set_position)

    #
    # Methods
    #

    def update(self, callback=None):
        """Force a player state and queue update"""
        Logr.debug("update")
        params = {}
        self.update_callback = callback

        if self.player_state is not None and self.player_state.version is not None:
            params['player_state_version'] = self.player_state.version

        if self.queue is not None and self.queue.version is not None:
            params['queue_version'] = self.queue.version

        self._sock._api_post('getPlayerState', params, False,
                             response_callback=self._update_callback)

    def _update_callback(self, result):
        Logr.debug("_update_callback")

        if result['status'] == 'error':
            raise RdioApiError(result)

        result = result['result']

        # Fire 'player_state' changed event
        if 'playerState' in result:
            self._field_changed('player_state', RdioPlayerState.parse(result['playerState']))
            Logr.debug("player_state updated to version %s", self.player_state.version)

        # Fire 'queue' changed event
        if 'queue' in result:
            self._field_changed('queue', RdioQueue.parse(result['queue']))
            Logr.debug("queue updated to version %s", self.queue.version)

        # Fire 'on_song_changed' event
        self._fire_on_song_changed(
            self.player_state.current_source.tracks[
                self.player_state.current_source.current_position])

        # Fire callback
        if self.update_callback is not None:
            self.update_callback(self.player_state, self.queue)
            self.update_callback = None

    def _fire_on_song_changed(self, track):
        """
        :type track: RdioTrack
        """
        fire = False
        if self._on_song_changed_last_fire is None:
            fire = True
        else:
            seconds = (time.time() - self._on_song_changed_last_fire)

            if seconds > SONG_CHANGED_MIN_SECONDS:
                fire = True
            elif self._on_song_changed_last_value is None:
                fire = True
            elif self._on_song_changed_last_value.key != track.key:
                fire = True

        if fire:
            self._on_song_changed_last_fire = time.time()
            self._on_song_changed_last_value = track
            self.on_song_changed(track)

    def get_playback_info(self, key, manual_play=True):
        """Get track playback info

        :param key: Track Key
        :type key: str
        """
        result = self._sock._api_post('getPlaybackInfo', {
            'key': key,
            'manualPlay': manual_play,
            'type': 'flash',
            'playerName': self._sock.pubsub.name,
            'requiresUnlimited': False
        }, secure=False)

        if result['status'] != 'ok':
            raise RdioApiError(result)

        return RdioPlaybackInfo.parse(result['result'])

    # Media Controls

    def toggle_pause(self):
        self._sock.services.private.publish_command('remote', 'togglePause')

    def toggle_shuffle(self):
        self._sock.services.private.publish_command('remote', 'toggleShuffle')

    def play(self):
        self._sock.services.private.publish_command('remote', 'play')

    def pause(self):
        self._sock.services.private.publish_command('remote', 'pause')

    def previous(self):
        self._sock.services.private.publish_command('remote', 'previous')

    def next(self):
        self._sock.services.private.publish_command('remote', 'next')

    def next_source(self):
        self._sock.services.private.publish_command('remote', 'nextSource')
