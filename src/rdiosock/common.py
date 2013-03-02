# Pattern used for pulling environment information from a web page
PATTERN_ENV = r'Env\s*=\s*\{\s*'\
              r'VERSION\s*:\s*(?P<version>\{.*?\})\s*,\s*'\
              r'currentUser\s*:\s*(?P<currentUser>\{.*?\})\s*,\s*'\
              r'serverInfo\s*:\s*(?P<serverInfo>\{.*?\})\s*\};'

PATTERN_CAMEL2SCORE_FIRST = r'(.)([A-Z][a-z]+)'
PATTERN_CAMEL2SCORE_ALL = r'([a-z0-9])([A-Z])'

URL_BASE = 'www.rdio.com'