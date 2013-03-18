RdioPlayer
=====================================

.. automodule:: rdiosock.player

    .. autoclass:: RdioPlayer

        **Fields**

        *Un-changeable fields updated via PubSub*

        .. py:attribute:: last_song_played

            :class:`rdiosock.objects.queue.RdioQueue`

            Last song played

        .. py:attribute:: last_song_play_time

        .. py:attribute:: last_source_played

            :class:`rdiosock.objects.source.RdioSource`

            Last source played

        .. py:attribute:: on_song_changed

            :class:`rdiosock.utils.EventHook`

            Song changed event

        .. py:attribute:: player_state

            :class:`rdiosock.objects.player_state.RdioPlayerState`

            Current Rdio player state

        .. py:attribute:: queue

            :class:`rdiosock.objects.queue.RdioQueue`

            Current Rdio player state

        **Properties**

        *Changeable properties updated and changed via PubSub*

        .. py:attribute:: volume

            :class:`float`

            Player volume (0.0 - 1.0)

            **NOTE:** This property sends pubsub messages

        .. py:attribute:: shuffle

            :class:`bool`

            Player shuffle mode

            **NOTE:** This property sends pubsub messages

        .. py:attribute:: repeat

            :class:`RdioPlayer.REPEAT_ALL`, :class:`RdioPlayer.REPEAT_ONE`, :class:`RdioPlayer.REPEAT_NONE`

            Player repeat mode

            **NOTE:** This property sends pubsub messages

        .. py:attribute:: position

            :class:`int`

            Player position in seconds

            **NOTE:** This property sends pubsub messages

        **Methods**

        .. automethod:: toggle_pause

        .. automethod:: toggle_shuffle

        .. automethod:: play

        .. automethod:: pause

        .. automethod:: previous

        .. automethod:: next

        .. automethod:: next_source