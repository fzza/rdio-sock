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