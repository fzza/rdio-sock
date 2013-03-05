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
import socket
from ws4py.client.threadedclient import WebSocketClient
from rdiosock.exceptions import RdioException, RdioApiError
from rdiosock.logr import Logr
from rdiosock.utils import camel_to_score, update_attrs, randint, random_id, EventHook


class RdioPubSub:
    def __init__(self, sock):
        self._sock = sock
        self.ws = None

        # Events
        self.on_connected = EventHook()

        # { "<topic>" : [<callbacks] }
        self._subscription_callbacks = {}

        # PubSub info
        self.topic = None
        self.token = None
        self.servers = None

    def connect(self, update=True):
        if self._sock.user.authorization_key is None or \
                self._sock.user.session_cookie is None:
            raise RdioException()

        if update:
            self.update_info()  # Update our PubSub info

        if self.token is None or self.token == '':
            raise RdioApiError()

        # Start up the WebSocket client
        self.ws = RdioPubSubClient(self, self.received_message, self.reconnect)
        self.ws.connect()

    def update_info(self):
        info_result = self._sock._api_post('pubsubInfo')

        if info_result['status'] == 'error':
            raise RdioApiError(info_result)

        Logr.debug('----------- PubSub ------------')
        update_attrs(self, info_result['result'], trace=True)

    def publish(self, topic, data):
        """Publish PubSub message

        @param topic: PubSub topic
        @type topic: str

        @param data: json serializable object
        @type data: object
        """
        self.ws.send_message(RdioPubSubMessage(
            RdioPubSubMessage.METHOD_PUB, topic, data
        ))

    def subscribe(self, service, target=None):
        """Subscribe to RdioService pubsub messages

        @param service: RdioService instance
        @type service: RdioService

        @param target: Target (User, Playlist) or None to indicate current user
        @type target: str or None
        """
        if target is None:
            target = self._sock.user.key
        service.__subscribe__(self, target)

    def subscribe_topic(self, topic, callback, target=None):
        """ Subscribe to pubsub messages

        @param topic: PubSub topic to subscribe to
        @type topic: str

        @param callback: callback(message) will be called when messages are received
        @type callback: function
        """
        topic = topic.strip('/')
        if '/' not in topic:
            if target is not None:
                topic = target + '/' + topic
            else:
                raise ValueError()

        if topic not in self._subscription_callbacks:
            self._subscription_callbacks[topic] = []

        if callback not in self._subscription_callbacks[topic]:
            self._subscription_callbacks[topic].append(callback)

        self.ws.send_message(RdioPubSubMessage(
            RdioPubSubMessage.METHOD_SUB, topic
        ))

        Logr.info("subscribed to %s", topic)

    def received_message(self, message):
        Logr.debug("received_message: %s", message)

        if message.method == RdioPubSubMessage.METHOD_CONNECTED:
            self.on_connected()
        elif message.method == RdioPubSubMessage.METHOD_PUB:
            # Send message to subscribed callbacks
            if message.topic in self._subscription_callbacks:
                for callback in self._subscription_callbacks[message.topic]:
                    callback(message)

    def reconnect(self):
        self.connect(False)


class RdioPubSubClient(WebSocketClient):
    def __init__(self, pubsub, received_message, reconnect):
        self.pubsub = pubsub
        self._received_message = received_message
        self._reconnect = reconnect

        super(RdioPubSubClient, self).__init__(self._select_random_server(False))

    def _select_random_server(self, parse=True):
        server_id = randint(0, len(self.pubsub.servers) - 1)
        self.url = 'ws://' + self.pubsub.servers[server_id]

        if parse:
            self._parse_url()

        Logr.info("selected server : %s", self.url)
        return self.url

    def send_message(self, message):
        Logr.debug("send_message %s", message)
        self.send(str(message))

    def opened(self):
        Logr.debug("opened")

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
        Logr.info("closed: (%s) %s", code, reason)

        if code == 1006:
            Logr.info("reconnecting")
            self._reconnect()

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

    SNIP_MIN_LENGTH = 100
    SNIP_STRING = "[...snip...]"

    def __init__(self, method, topic, data=None):
        self.method = method
        self.topic = topic
        self.data = data

    @staticmethod
    def parse(message):
        message = message.split(' ', 1)
        if len(message) != 2:
            Logr.warning("invalid message")
            Logr.debug("len(message)= %s", len(message))
            Logr.debug(message)
            return None
        method, data = message

        # Check if method is valid
        if method not in RdioPubSubMessage.METHODS:
            Logr.warning('invalid message method "%s"', method)
            return None

        if '|' not in data:
            return RdioPubSubMessage(method, data)

        topic, data = data.split('|', 1)

        return RdioPubSubMessage(method, topic, json.loads(data))

    def __str__(self):
        if self.data:
            data_str = json.dumps(self.data)
            if len(data_str) >= self.SNIP_MIN_LENGTH:
                part_length = (self.SNIP_MIN_LENGTH / 2) - (len(self.SNIP_STRING) / 2)
                data_str = "".join([
                    data_str[:part_length],
                    self.SNIP_STRING,
                    data_str[-part_length:]
                ])
            return self.method + ' ' + self.topic + '|' + data_str
        else:
            return self.method + ' ' + self.topic
