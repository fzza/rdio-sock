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


class RdioService(object):
    __topic__ = None

    def __init__(self, sock):
        self._sock = sock

    def publish(self, data):
        self._sock.pubsub.publish(self._sock.user.key + '/' + self.__topic__, data)

    def publish_event(self, event, data=None):
        if data is None:
            data = {}

        data['event'] = event

        self.publish(data)

    def received_message(self, message):
        raise NotImplementedError()

    def __subscribe__(self, pubsub, target):
        """Subscribe service to pubsub messages

        @param pubsub: Rdio pubsub instance
        @type pubsub: RdioPubSub

        @param target: Topic target
        @type target: str
        """

        if self.__topic__ is None:
            raise NotImplementedError()

        pubsub.subscribe_topic(self.__topic__, self.received_message, target)
