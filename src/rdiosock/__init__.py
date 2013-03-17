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


import re
import datetime
import requests
import time
from rdiosock import syrequests
from rdiosock.common import PATTERN_ENV
from rdiosock.logr import Logr
from rdiosock.metadata import RdioMetadata
from rdiosock.player import RdioPlayer
from rdiosock.services.fields import RdioFieldService
from rdiosock.services.private import RdioPrivateService
from rdiosock.pubsub import RdioPubSub
from rdiosock.user import RdioUser
from rdiosock.server_info import RdioServerInfo
from rdiosock.utils import parse_json, api_url, return_data_type


DEFAULT_USERAGENT_CHROME = "Mozilla/5.0 (Windows NT 6.2; WOW64) " \
                           "AppleWebKit/537.22 (KHTML, like Gecko) " \
                           "Chrome/25.0.1364.97 " \
                           "Safari/537.22"


class RdioSock:
    def __init__(self, useragent=DEFAULT_USERAGENT_CHROME):
        self._useragent = useragent

        self.pubsub = RdioPubSub(self)
        self.services = RdioSockServiceManager(self)

        self.metadata = RdioMetadata(self)
        self.player = RdioPlayer(self)
        self.user = RdioUser(self)
        self.server_info = RdioServerInfo(self)

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

    def _api_get(self, method, params=None, secure=True, response_callback=None,
                 return_type='json', extras=None):
        return return_data_type(
            self._api_request(method, 'GET', params, secure, response_callback, extras),
            return_type
        )

    def _api_post(self, method, params=None, secure=True, response_callback=None,
                  return_type='json', extras=None):
        return return_data_type(
            self._api_request(method, 'POST', params, secure, response_callback, extras),
            return_type
        )

    def _api_request(self, method, http_method, params=None, secure=True,
                     response_callback=None, extras=None):
        url = api_url(method, secure)

        Logr.debug("_api_request, url = %s", url)
        start = time.time()

        if extras is None:
            extras = []

        # Params
        if params is None:
            params = {}

        extras.append('*.WEB')
        params['extras[]'] = extras

        params['method'] = method
        params['v'] = '20130124'

        if self.user.authorization_key is not None:
            params['_authorization_key'] = self.user.authorization_key

        # Cookies
        cookies = {}

        if self.user.session_cookie is not None:
            cookies['r'] = self.user.session_cookie

        # Headers
        headers = {}

        if self._useragent is not None:
            headers['User-Agent'] = self._useragent

        job = syrequests.request(
            http_method, url,
            data=params,
            cookies=cookies,
            headers=headers
        )

        if response_callback is None:
            result = job.execute_sync()
        else:
            job.execute(response_callback)
            result = job

        Logr.debug("_api_request, elapsed = %.0fms",
                   datetime.timedelta(
                       seconds=time.time() - start).total_seconds() * 1000)

        return result


class RdioSockServiceManager:
    def __init__(self, sock):
        self._sock = sock

        # Services
        self.fields = RdioFieldService(self._sock)
        self.private = RdioPrivateService(self._sock)
