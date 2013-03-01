import json
import requests
from rdiosock.exceptions import RdioException


class Api:
    def __init__(self, sock):
        self.sock = sock

    def get(self, method, params=None, secure=True, data_type='json'):
        return self._return(self.request(method, params, 'GET', secure), data_type)

    def post(self, method, params=None, secure=True, data_type='json'):
        return self._return(self.request(method, params, 'POST', secure), data_type)

    def _return(self, request, data_type):
        if data_type == 'request':
            return request

        if data_type == 'json':
            if request.status_code != 200:
                raise RdioException()
            return json.loads(request.text)

        raise ValueError()

    def request(self, method, params, http_method, secure=True):
        url = self.sock._get_api_url(method, secure)

        if params is None:
            params = {}

        params['extras[]'] = '*.WEB'
        params['method'] = method

        cookies = {}

        # Set the authorizationKey if we have an environment
        if self.sock.web.isEnvironmentPresent():
            params['_authorization_key'] = self.sock.web.env['currentUser']['authorizationKey']

        # Set our session cookie if we are signed in
        if self.sock.web.isSignedIn():
            cookies['r'] = self.sock.web.r

        return requests.request(http_method, url, data=params, cookies=cookies)