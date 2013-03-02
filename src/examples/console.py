import os
import sys
from rdiosock.exceptions import RdioException

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))
from rdiosock import RdioSock

if __name__ == '__main__':
    rdio = RdioSock()

    username = None
    password = None

    # Read auth from /console.auth
    auth_path = os.path.dirname(__file__) + "/console.auth"
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

    rdio.pubsub.connect()  # Connect the pubsub client