from pprint import pprint
import requests
from rdiosock.exceptions import RdioApiError, RdioNetworkError
from rdiosock.utils import web_url, camel_to_score, update_attrs


class RdioUser:
    def __init__(self, sock):
        self._sock = sock

        # Environment Information
        self.env_loaded = False
        self.session_cookie = None  # HTTP session cookie

        # - Internal Data
        self.id = None
        self.key = None
        self.authorization_key = None

        #  - User Details
        self.first_name = None
        self.last_name = None
        self.vanity_name = None

        # - State details
        self.is_anonymous = None
        self.new_user = None

    def login(self, username, password, remember=True):
        if not self.env_loaded or self.authorization_key is None:
            self._sock._update_env(url=web_url('account/signin'))

        print "--> user.login"

        # API 'signIn' request (get the redirect_url)
        signin_result = self._sock._api_post('signIn', {
            'username': username,
            'password': password,
            'remember': int(remember),
            'nextUrl': '',
            'v': '20130124'
        })

        if signin_result.get('status') != 'ok':
            raise RdioApiError(signin_result)

        if not 'result' in signin_result or \
                not signin_result['result'].get('success', False):
            raise RdioApiError()

        redirect_url = signin_result['result'].get('redirect_url')
        if redirect_url is None or redirect_url == '':
            raise RdioApiError()

        print 'redirect_url', ':', redirect_url

        # Web redirect request (get the session_cookie)
        redirect_result = requests.get(redirect_url)

        if redirect_result.status_code != 200:
            raise RdioNetworkError("HTTP request returned an unexpected status_code", redirect_result.status_code)

        if len(redirect_result.history) != 1 or \
                redirect_result.history[0].status_code != 302 or \
                'r' not in redirect_result.history[0].cookies:
            raise RdioNetworkError("Missing session cookie")

        # TODO: Store the cookie for later use
        self.session_cookie = redirect_result.history[0].cookies['r']
        print 'session_cookie', ':', self.session_cookie

        self._sock._update_env(data=redirect_result.text)

    def _load_env(self, currentUser):
        print '------------- User ------------'
        update_attrs(self, currentUser, trace=True)
        print '-------------------------------'