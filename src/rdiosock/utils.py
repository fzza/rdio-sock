import json
from random import Random
import re
from rdiosock.common import URL_BASE, PATTERN_CAMEL2SCORE_FIRST, PATTERN_CAMEL2SCORE_ALL
from rdiosock.exceptions import RdioNetworkError


#
# URL creation
#

def api_url(method, secure=True):
    return web_url('api/1') + method


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
                print name, ':', value

def parse_json(data, default=None):
    o = default
    try:
        o = json.loads(data)
    except ValueError:
        pass
    return o


def return_data_type(request, return_type):
    if return_type == 'request':
        return request

    if return_type == 'json':
        if request.status_code != 200:
            raise RdioNetworkError("HTTP request returned an unexpected status_code", request.status_code)
        return json.loads(request.text)

    raise ValueError()