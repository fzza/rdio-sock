class RdioRemote(object):
    REPEAT_ALL = 2
    REPEAT_ONE = 1
    REPEAT_NONE = 0

    def __init__(self, sock):
        self._sock = sock

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
        if repeat_type not in [RdioRemote.REPEAT_ALL,
                               RdioRemote.REPEAT_ONE,
                               RdioRemote.REPEAT_NONE]:
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
