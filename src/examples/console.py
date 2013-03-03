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


import code
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(current_dir + "\\..\\"))

from rdiosock import RdioSock
from rdiosock.exceptions import RdioException

rdio = RdioSock()


def login():
    username = None
    password = None

    # Read auth from /console.auth
    auth_path = current_dir + "/console.auth"
    if os.path.exists(auth_path):
        fp = open(auth_path)
        data = fp.read()
        fp.close()
        username, password = data.split(':')

    # Username console input
    if username is None:
        username = raw_input('Username: ')

    # Password console input
    if password is None:
        password = raw_input('Password: ')

    # Login to Rdio
    try:
        rdio.user.login(username, password)
    except RdioException, e:
        print 'failed to login, unable to continue'
        raise


def connected(message):
    print "connected"

if __name__ == '__main__':
    login()
    rdio.pubsub.connect(connected)

    code.interact(local=globals())
