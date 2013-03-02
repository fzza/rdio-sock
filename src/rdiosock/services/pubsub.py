import json
from ws4py.client.threadedclient import WebSocketClient
from rdiosock.exceptions import RdioException, RdioApiError
from rdiosock.utils import camel_to_score, update_attrs, randint, random_id


class RdioPubSub:
    def __init__(self, sock):
        self._sock = sock
        self.ws = None

        # PubSub info
        self.topic = None
        self.token = None
        self.servers = None

    def connect(self):
        if self._sock.user.authorization_key is None or \
                self._sock.user.session_cookie is None:
            raise RdioException()

        self.update_info()  # Update our PubSub info

        if self.token is None or self.token == '':
            raise RdioApiError()

        # Start up the WebSocket client
        self.ws = RdioPubSubClient(self._sock)
        self.ws.connect()

    def update_info(self):
        info_result = self._sock._api_post('pubsubInfo')

        if info_result['status'] == 'error':
            raise RdioApiError(info_result)

        print '----------- PubSub ------------'
        update_attrs(self, info_result['result'], trace=True)
        print '-------------------------------'


class RdioPubSubClient(WebSocketClient):
    def __init__(self, sock):
        self._sock = sock

        # Choose a random server
        server_id = randint(0, len(self._sock.pubsub.servers) - 1)
        self.current_server = self._sock.pubsub.servers[server_id]
        print "[RdioPubSubClient] using server :", self.current_server

        super(RdioPubSubClient, self).__init__('ws://' + self.current_server)

    # PubSub methods

    def pub(self, key, data):
        pass

    def sub(self, key):
        pass

    def send_message(self, method, key, data=None):
        print "[RdioPubSubClient] send_message", method, key

        message = method + ' ' + key
        if data is not None:
            message += '|' + json.dumps(data)

        self.send(message)

    # WebSocket callbacks

    def opened(self):
        print "[RdioPubSubClient] opened"

        self.send_message('CONNECT', self._sock.pubsub.token, {
            'chat': {
                'canChat': True
            },
            'player': {
                'canRemote': True,
                'name': '_web_' + str(random_id())
            }
        })

    def closed(self, code, reason=None):
        print "[RdioPubSubClient] closed:", code, reason

    def received_message(self, message):
        print "[RdioPubSubClient] received_message:", message