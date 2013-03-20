Rdio-Sock Documentation
=====================================

Start with the following example:
::

    rdio = RdioSock()

    # Login to Rdio
    rdio.user.login("<username>", "<password>")

    # Song changed callback
    def song_changed(track):
        print "%s - %s - %s" % (track.name, track.album, track.artist)

    # PubSub connected callback
    def pubsub_connected():
        # Subscribe services into pubsub updates
        rdio.pubsub.subscribe(rdio.services.fields)
        rdio.pubsub.subscribe(rdio.services.private)

        # Bind player events
        rdio.player.on_song_changed.bind(song_changed)

        # Force a player update to get the current state
        # (Updates after this are done via PubSub automatically)
        rdio.player.update()

    rdio.pubsub.on_connected.bind(pubsub_connected)

    # Connect the WebSocket-PubSub client to enable real-time updates
    rdio.pubsub.connect()


Classes
=====================================

Core:

.. toctree::
    :maxdepth: 2

    rdiosock
    rdiosock/metadata
    rdiosock/player
    rdiosock/pubsub
    rdiosock/server_info
    rdiosock/user

Services:

.. toctree::
    :maxdepth: 2

    rdiosock/services/fields
    rdiosock/services/private

Objects:

.. toctree::
    :maxdepth: 2

    rdiosock/objects/base
    rdiosock/objects/album
    rdiosock/objects/artist
    rdiosock/objects/collection
    rdiosock/objects/person
    rdiosock/objects/player_state
    rdiosock/objects/queue
    rdiosock/objects/source
    rdiosock/objects/track

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

