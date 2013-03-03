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


import json
from ws4py.client.threadedclient import WebSocketClient
from rdiosock.exceptions import RdioException, RdioApiError
from rdiosock.utils import camel_to_score, update_attrs, randint, random_id


class RdioPubSub:
    def __init__(self, sock):
        self._sock = sock
        self.ws = None

        # Callbacks
        self.connected_callback = None

        # PubSub info
        self.topic = None
        self.token = None
        self.servers = None

    def connect(self, connected_callback=None):
        if self._sock.user.authorization_key is None or \
                self._sock.user.session_cookie is None:
            raise RdioException()

        self.connected_callback = connected_callback

        self.update_info()  # Update our PubSub info

        if self.token is None or self.token == '':
            raise RdioApiError()

        # Start up the WebSocket client
        self.ws = RdioPubSubClient(self, self.received_message)
        self.ws.connect()

    def update_info(self):
        info_result = self._sock._api_post('pubsubInfo')

        if info_result['status'] == 'error':
            raise RdioApiError(info_result)

        print '----------- PubSub ------------'
        update_attrs(self, info_result['result'], trace=True)
        print '-------------------------------'

    def publish(self, topic, data):
        self.ws.send_message(RdioPubSubMessage(
            RdioPubSubMessage.METHOD_PUB, topic, data
        ))

    def subscribe(self, topic):
        self.ws.send_message(RdioPubSubMessage(
            RdioPubSubMessage.METHOD_SUB, topic
        ))

    def received_message(self, message):
        print "[RdioPubSub] received_message:", message

        if message.method == RdioPubSubMessage.METHOD_CONNECTED:
            # Call the connected_callback
            if self.connected_callback is not None:
                self.connected_callback(message)

        elif message.method == RdioPubSubMessage.METHOD_PUB:
            pass


class RdioPubSubClient(WebSocketClient):
    def __init__(self, pubsub, received_message):
        self.pubsub = pubsub

        self._received_message = received_message

        # Choose a random server
        server_id = randint(0, len(self.pubsub.servers) - 1)
        self.current_server = self.pubsub.servers[server_id]
        print "[RdioPubSubClient] using server :", self.current_server

        super(RdioPubSubClient, self).__init__('ws://' + self.current_server)

    def send_message(self, message):
        print "[RdioPubSubClient] send_message", message
        self.send(str(message))

    def opened(self):
        print "[RdioPubSubClient] opened"

        self.send_message(RdioPubSubMessage(
            RdioPubSubMessage.METHOD_CONNECT, self.pubsub.token, {
                'chat': {
                    'canChat': True
                },
                'player': {
                    'canRemote': True,
                    'name': '_web_' + str(random_id())
                }
        }))

    def closed(self, code, reason=None):
        print "[RdioPubSubClient] closed:", code, reason

    def received_message(self, message):
        self._received_message(RdioPubSubMessage.parse(str(message)))


class RdioPubSubMessage:
    METHOD_CONNECT = 'CONNECT'
    METHOD_CONNECTED = 'CONNECTED'

    METHOD_PUB = 'PUB'
    METHOD_SUB = 'SUB'
    METHODS = (
        METHOD_CONNECT,
        METHOD_CONNECTED,
        METHOD_PUB,
        METHOD_SUB
    )

    def __init__(self, method, topic, data=None):
        self.method = method
        self.topic = topic
        self.data = data

    @staticmethod
    def parse(message):
        message = message.split(' ')
        if len(message) != 2:
            print 'ERROR:', 'invalid message'
            return None
        method, data = message

        # Check if method is valid
        if method not in RdioPubSubMessage.METHODS:
            print 'ERROR:', 'invalid message method', '"' + method + '"'
            return None

        if '|' not in data:
            return RdioPubSubMessage(method, data)

        topic, data = data.split('|')

        return RdioPubSubMessage(method, topic, json.loads(data))

    def __str__(self):
        if self.data:
            return self.method + ' ' + self.topic + '|' + json.dumps(self.data)
        else:
            return self.method + ' ' + self.topic

