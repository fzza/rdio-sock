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
from rdiosock.utils import EventHook, camel_to_score


class RdioPlayer(EventHook):
    REPEAT_ALL = 2
    REPEAT_ONE = 1
    REPEAT_NONE = 0

    def __init__(self, sock):
        """
        @type sock: RdioSock
        """
        super(RdioPlayer, self).__init__()
        self._sock = sock

        # fields
        self.last_song_played = None

        # Bind field events
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSongPlayed')
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSourcePlayed')
        self._sock.services.fields.on_changed.bind(self._field_changed, 'lastSongPlayTime')

    def _field_changed(self, name, value):
        name = camel_to_score(name)

        print '_field_changed(%s) : ' % name,
        if hasattr(self, name):
            setattr(self, name, value)
            print 'updated'
        else:
            print 'not found'
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
    # Media Controls
    #

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