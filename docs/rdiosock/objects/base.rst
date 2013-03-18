RdioMediaItem
=====================================

.. automodule:: rdiosock.objects.base

    .. autoclass:: RdioMediaItem

        .. begin-RdioMediaItem

        .. py:attribute:: can_sample

            :class:`bool`

        .. py:attribute:: can_stream

            :class:`bool`

        .. py:attribute:: can_tether

            :class:`bool`

        .. py:attribute:: is_clean

            :class:`bool`

        .. py:attribute:: is_explicit

            :class:`bool`

        .. py:attribute:: duration

            :class:`int`

        .. py:attribute:: price

            :class:`float`

        .. py:attribute:: embed_url

            :class:`str`

        .. py:attribute:: iframe_url

            :class:`str`

        .. end-RdioMediaItem

RdioNamedItem
=====================================

.. autoclass:: RdioNamedItem

    .. begin-RdioNamedItem

    .. py:attribute:: name

        :class:`str`

    .. py:attribute:: length

        :class:`int`

    .. py:attribute:: short_url

        :class:`str`

    .. end-RdioNamedItem

RdioIconItem
=====================================

.. autoclass:: RdioIconItem

    .. begin-RdioIconItem

    .. py:attribute:: base_icon

        :class:`str`

    .. py:attribute:: icon

        :class:`str`

    .. end-RdioIconItem

RdioDataItem
=====================================

.. autoclass:: RdioDataItem

    .. begin-RdioDataItem

    .. py:attribute:: key

        :class:`str`

    .. py:attribute:: type

        :class:`str`

    .. py:attribute:: url

        :class:`str`

    .. end-RdioDataItem

RdioBaseItem
=====================================

.. autoclass:: RdioBaseItem

    .. begin-RdioBaseItem

    .. automethod:: parse

    .. end-RdioBaseItem