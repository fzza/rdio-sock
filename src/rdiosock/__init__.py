import re
import requests
from rdiosock.common import PATTERN_ENV
from rdiosock.remote import RdioRemote
from rdiosock.services.pubsub import RdioPubSub
from rdiosock.user import RdioUser
from rdiosock.server_info import RdioServerInfo
from rdiosock.utils import parse_json, api_url, return_data_type


class RdioSock:
    def __init__(self):
        self.remote = RdioRemote(self)
        self.user = RdioUser(self)
        self.server_info = RdioServerInfo(self)

        # Services
        self.pubsub = RdioPubSub(self)

        # Environment Information
        self.env_loaded = False
        self.version = None

    #
    # Environment
    #

    def _update_env(self, url=None, data=None):
        if url is None and data is None:
            raise ValueError()  # One parameter required
        if url is not None and data is not None:
            raise ValueError()  # Only one parameter can be used

        # request the 'url'
        if url is not None:
            r = requests.get(url)
            if r.status_code != 200:
                raise ValueError()
            data = r.text

        match = re.search(PATTERN_ENV, data, re.DOTALL | re.IGNORECASE | re.MULTILINE)

        # Parse groups json into objects
        version = parse_json(match.group('version'), {})
        currentUser = parse_json(match.group('currentUser'), {})
        serverInfo = parse_json(match.group('serverInfo'), {})

        # Update environment objects
        self._load_env(version)
        self.user._load_env(currentUser)
        self.server_info._load_env(serverInfo)

    def _load_env(self, version):
        self.version = version.get('version')
        self.env_loaded = True

    #
    # API
    #

    def _api_get(self, method, params=None, secure=True, return_type='json'):
        return return_data_type(self._api_request(method, 'GET', params, secure), return_type)

    def _api_post(self, method, params=None, secure=True, return_type='json'):
        return return_data_type(self._api_request(method, 'POST', params, secure), return_type)

    def _api_request(self, method, http_method, params=None, secure=True):
        url = api_url(method, secure)

        if params is None:
            params = {}

        params['extras[]'] = '*.WEB'
        params['method'] = method

        cookies = {}

        if self.user.authorization_key is not None:
            params['_authorization_key'] = self.user.authorization_key

        if self.user.session_cookie is not None:
            cookies['r'] = self.user.session_cookie

        return requests.request(http_method, url, data=params, cookies=cookies)