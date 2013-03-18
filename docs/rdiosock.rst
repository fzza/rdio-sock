RdioSock
=====================================

.. automodule:: rdiosock

    .. autoclass:: RdioSock

        **Fields**

        .. py:attribute:: pubsub

            :class:`rdiosock.pubsub.RdioPubSub`

            PubSub client

        .. py:attribute:: services

            :class:`rdiosock.RdioSockServiceManager`

            Rdio service manager

        .. py:attribute:: metadata

            :class:`rdiosock.metadata.RdioMetadata`

        .. py:attribute:: player

            :class:`rdiosock.player.RdioPlayer`

        .. py:attribute:: user

            :class:`rdiosock.user.RdioUser`

        .. py:attribute:: server_info

            :class:`rdiosock.server_info.RdioServerInfo`

        .. py:attribute:: version

            :class:`int`

            Rdio communication version

    .. autoclass:: RdioSockServiceManager

        **Fields**

        .. py:attribute:: fields

            :class:`rdiosock.services.fields.RdioFieldService`

            Field service manager

        .. py:attribute:: private

            :class:`rdiosock.services.private.RdioPrivateService`

            Private service manager
