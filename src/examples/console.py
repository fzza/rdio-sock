import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

from rdiosock import RdioSock

if __name__ == '__main__':
    username = None
    password = None

    # look in /auth file for username and password
    auth_path = os.path.dirname(__file__) + "/auth"
    if os.path.exists(auth_path):
        fp = open(auth_path)
        data = fp.read()
        fp.close()
        username, password = data.split(':')

    # no /auth file, ask for username and password input
    nl = False
    if username is None or username == '':
        username = raw_input('Username: ')
        nl = True

    if password is None or password == '':
        password = raw_input('Password: ')
        nl = True

    if nl:
        print

    print "Logging in with..."
    print 'Username =', username
    print 'Password =', '*' * len(password)
    print '-------------------------------------'

    rdio = RdioSock()
    rdio.connect(username, password)

    while True:
        if raw_input() == 'exit':
            break