RdioAlbum
=====================================

.. automodule:: rdiosock.objects.album

    .. autoclass:: RdioAlbum

        .. py:attribute:: artist

            :class:`str`

        .. py:attribute:: artist_key

            :class:`str`

        .. py:attribute:: artist_url

            :class:`str`

        .. py:attribute:: big_icon

            :class:`str`

        .. py:attribute:: big_icon_1200

            :class:`str`

        .. py:attribute:: copyright

            :class:`str`

        .. py:attribute:: display_date

            :class:`unknown`

        .. py:attribute:: icon_400

            :class:`str`

        .. py:attribute:: labels

            :class:`unknown`

        .. py:attribute:: network_consumers

            list of :class:`rdiosock.objects.person.RdioPerson`

        .. py:attribute:: playlist_count

            :class:`int`

        .. py:attribute:: play_count

            :class:`int`

        .. py:attribute:: release_date

            :class:`unknown`

        .. py:attribute:: review

            :class:`str`

        .. py:attribute:: tracks

            list of :class:`rdiosock.objects.track.RdioTrack`

        .. py:attribute:: track_keys

            list of :class:`str`

        .. automethod:: parse_tracks

        **RdioMediaItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioMediaItem
            :end-before: end-RdioMediaItem

        **RdioNamedItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioNamedItem
            :end-before: end-RdioNamedItem

        **RdioIconItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioIconItem
            :end-before: end-RdioIconItem

        **RdioDataItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioDataItem
            :end-before: end-RdioDataItem

        **RdioBaseItem**
        *(Inherited)*

        .. include:: /rdiosock/objects/base.rst
            :start-after: begin-RdioBaseItem
            :end-before: end-RdioBaseItem