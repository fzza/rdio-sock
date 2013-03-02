from pprint import pprint
from rdiosock.utils import camel_to_score, update_attrs


class RdioServerInfo:
    def __init__(self, sock):
        self._sock = sock

        # Environment Information
        self.env_loaded = False

        self.country_code = None
        self.country_name = None
        self.locale = None

    def _load_env(self, serverInfo):
        print '--------- ServerInfo ----------'
        update_attrs(self, serverInfo, trace=True)
        print '-------------------------------'