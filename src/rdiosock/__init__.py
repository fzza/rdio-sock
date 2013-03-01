from rdiosock.api import Api
from rdiosock.pubsub import PubSub
from rdiosock.web import Web


class RdioSock:
    API_URL = 'www.rdio.com/api/1'
    WEB_URL = 'www.rdio.com'

    def __init__(self):
        self.api = Api(self)
        self.pubSub = PubSub(self)
        self.web = Web(self)

    def connect(self, username, password):
        self.web.signIn(username, password)
        print '-------------------------------------'
        self.pubSub.connect()

    def _get_api_url(self, method, secure=True):
        url = 'https://'
        if not secure:
            url = 'http://'
        return url + self.API_URL + '/' + method

    def _get_web_url(self, suffix, secure=True):
        url = 'https://'
        if not secure:
            url = 'http://'
        if not suffix.startswith('/'):
            suffix = '/' + suffix
        return url + self.WEB_URL + suffix
