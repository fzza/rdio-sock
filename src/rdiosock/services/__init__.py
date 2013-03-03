class RdioService(object):
    __key__ = None

    def __init__(self, sock):
        self._sock = sock

    def publish(self, data):
        self._sock.pubsub.publish(self._sock.user.key + '/' + self.__key__, data)

    def publish_event(self, event, data=None):
        if data is None:
            data = {}

        data['event'] = event

        self.publish(data)