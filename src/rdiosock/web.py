import json
from pprint import pprint
import re
import requests
from rdiosock.exceptions import RdioException


# Pattern used for pulling version, currentUser and serverInfo from a web page

ENV_PATTERN = r'Env\s*=\s*\{\s*'\
              r'VERSION\s*:\s*(?P<version>\{.*?\})\s*,\s*'\
              r'currentUser\s*:\s*(?P<currentUser>\{.*?\})\s*,\s*'\
              r'serverInfo\s*:\s*(?P<serverInfo>\{.*?\})\s*\};'


class Web:
    def __init__(self, sock):
        self.sock = sock

        self.env = None
        self.r = None

    def signIn(self, username, password, remember=True):
        self.r = None  # Reset our session cookie 'r'

        self.requestEnv(self.sock._get_web_url('account/signin/'))
        print 'authorizationKey', '=', self.env['currentUser']['authorizationKey']

        # Call the signIn method with our username and password
        signin_result = self.sock.api.post('signIn', {
            'username': username,
            'password': password,
            'remember': int(remember),
            'nextUrl': '',
            'v': '20130124'
        })

        if signin_result['status'] == 'error':
            raise RdioException(signin_result)

        if not signin_result['result']['success']:
            raise RdioException()

        print 'redirect_url ', '=', signin_result['result']['redirect_url']

        # Call redirect_url and store the session cookie
        redirect_result = requests.get(signin_result['result']['redirect_url'])

        if redirect_result.status_code != 200:
            raise RdioException()

        if len(redirect_result.history) != 1:
            raise RdioException()

        if redirect_result.history[0].status_code != 302:
            raise RdioException()

        if not 'r' in redirect_result.history[0].cookies:
            raise RdioException()

        self.r = redirect_result.history[0].cookies['r']
        print 'r', '=', self.r

        self.updateEnv(redirect_result.text)

        print '-------------------------------------'
        print "key =", self.env['currentUser']['key']
        print "first_name =", self.env['currentUser']['first_name']
        print "last_name =", self.env['currentUser']['last_name']
        print "vanity_name =", self.env['currentUser']['vanity_name']

    def requestEnv(self, url):
        return self.updateEnv(requests.get(url).text)

    def updateEnv(self, data):
        match = re.search(ENV_PATTERN, data, re.DOTALL | re.IGNORECASE | re.MULTILINE)

        self.env = {
            'version': self._parseJson(match.group('version')),
            'currentUser': self._parseJson(match.group('currentUser')),
            'serverInfo': self._parseJson(match.group('serverInfo'))
        }

    def isEnvironmentPresent(self):
        if self.env is None:
            return False

        if 'currentUser' not in self.env:
            return False

        return 'authorizationKey' in self.env['currentUser']

    def isSignedIn(self):
        if not self.isEnvironmentPresent():
            return False

        if not 'isAnonymous' in self.env['currentUser']:
            return False

        return not self.env['currentUser']['isAnonymous']

    def _parseJson(self, s, default=None):
        o = default
        try:
            o = json.loads(s)
        except ValueError:
            pass
        return o
