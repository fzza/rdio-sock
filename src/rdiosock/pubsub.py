import json
from ws4py.client.threadedclient import WebSocketClient
from rdiosock import bujagali
from rdiosock.exceptions import RdioException


class PubSub:
    def __init__(self, sock):
        self.sock = sock
        self.ws = None

        self.info = None

    def connect(self):
        if not self.sock.web.isSignedIn():
            raise RdioException()

        self.requestInfo()

        # Start up a WebSocket client
        self.ws = PubSubClient(self)
        self.ws.connect()

    def _ready(self):
        self.ws.pub(self.sock.web.env['currentUser']['key'] + '/private', {
            'event': 'remote',
            'command': {
                'type': 'togglePause'
            }
        })
        #self.ws.sub(self.sock.web.env['currentUser']['key'] + '/presence')

    def requestInfo(self):
        self.info = None  # Reset our current info

        if self.sock.web.r is None or self.sock.web.env is None:
            raise RdioException()

        info_result = self.sock.api.post('pubsubInfo')

        if info_result['status'] == 'error':
            raise RdioException(info_result)

        self.info = info_result['result']


class PubSubClient(WebSocketClient):
    def __init__(self, pubSub):
        self.pubSub = pubSub

        if self.pubSub.info is None:
            raise RdioException()

        # choose a server
        x = bujagali.utils.randomID(len(self.pubSub.info['servers']) - 1)
        url = 'ws://' + self.pubSub.info['servers'][x]
        print "using pubSub server:", url

        super(PubSubClient, self).__init__(url)

    def pub(self, key, data):
        self.sendMessage('PUB', key, data)

    def sub(self, key):
        self.sendMessage('SUB', key)

    def sendMessage(self, method, key, data=None):
        print "]> " + method + ' ' + key

        message = method + ' ' + key
        if data is not None:
            message += '|' + json.dumps(data)

        self.send(message)

    def opened(self):
        print "connection opened..."

        # Send the connect request
        self.sendMessage('CONNECT', self.pubSub.info['token'], {
            'chat': {
                'canChat': True
            },
            'player': {
                'canRemote': True,
                'name': '_web_' + str(bujagali.utils.randomID())
            }
        })

        self.pubSub._ready()

    def closed(self, code, reason=None):
        print "closed", code, reason

    def received_message(self, message):
        print "received_message"
        print '\t', message