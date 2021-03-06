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
from random import Random
import re
from requests import Response
from rdiosock.common import URL_BASE, PATTERN_CAMEL2SCORE_FIRST, PATTERN_CAMEL2SCORE_ALL
from rdiosock.exceptions import RdioNetworkError


#
# URL creation
#
from rdiosock.logr import Logr


def api_url(method, secure=True):
    return web_url('api/1', secure) + method


def web_url(suffix, secure=True):
    url = 'https://'
    if not secure:
        url = 'http://'

    if not suffix.startswith('/'):
        suffix = '/' + suffix

    if not suffix.endswith('/'):
        suffix += '/'

    return url + URL_BASE + suffix


#
# Random
#

_random = Random()


def randint(a, b):
    return _random.randint(a, b)


def random_id():
    return randint(0, 10000000)


# EventHook

class EventHook(object):
    def __init__(self):
        # { <subject> : [ <handler> ] }
        self.__handlers = {}

    def bind(self, handler, subject=None):
        if subject not in self.__handlers:
            self.__handlers[subject] = []

        self.__handlers[subject].append(handler)

    def unbind(self, handler):
        subject = None
        found = False

        for subject, handlers in self.__handlers.items():
            for h in handlers:
                if h == handler:
                    found = True
                    break

        if not found:
            raise ValueError()

        self.__handlers[subject].remove(handler)

        if len(self.__handlers[subject]) == 0:
            del self.__handlers[subject]

    def __getitem__(self, subject):
        if subject in self.__handlers:
            return FunctionListWrapper(self.__handlers[subject])
        return FunctionListWrapper()

    def __call__(self, *args, **kwargs):
        for subject, handlers in self.__handlers.items():
            for handler in handlers:
                handler(*args, **kwargs)


class FunctionListWrapper(object):
    def __init__(self, functions=None):
        if functions is None:
            functions = []

        self.functions = functions

    def __call__(self, *args, **kwargs):
        for function in self.functions:
            function(*args, **kwargs)


#
# Other Utils
#

def camel_to_score(name):
    s1 = re.sub(PATTERN_CAMEL2SCORE_FIRST, r'\1_\2', name)
    return re.sub(PATTERN_CAMEL2SCORE_ALL, r'\1_\2', s1).lower()


def update_attrs(obj, attr_dict, trace=False):
    for key, value in attr_dict.items():
        name = camel_to_score(key)
        if hasattr(obj, name):
            setattr(obj, name, value)
            if trace:
                Logr.debug('%s : %s', name, value)


def parse_json(data, default=None):
    o = default
    try:
        o = json.loads(data)
    except ValueError:
        pass
    return o


def return_data_type(request, return_type='json'):
    if type(request) is Response and return_type == 'json':
        if request.status_code != 200:
            raise RdioNetworkError("HTTP request returned an unexpected status_code", request.status_code)
        return json.loads(request.text)

    return request
