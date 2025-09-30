import os
import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions on ftp_homedir directory
ftp_homedir = '/home/files'
os.makedirs(ftp_homedir, exist_ok=True) # create dir if doesn't exist
authorizer.add_user('guest', '', ftp_homedir, perm='elradfmwMT')

# Define a readonly anonymous user
# authorizer.add_anonymous(os.getcwd())

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Define a customized banner (string returned when client connects)
handler.banner = "pyftpdlib based FTP server ready."

# Specify a masquerade address and the range of ports to use for
# passive connections.  Decomment in case you're behind a NAT.
# handler.masquerade_address = '127.0.0.1'
handler.passive_ports = range(60000, 60010) # type: ignore

# Instantiate FTP server class and listen on all interfaces, port 2121
address = ('', 21)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# logging mode
logging.basicConfig(level=logging.DEBUG)

# start ftp server
try:
    print("FTP server running...")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nStopping FTP server...")
    server.close_all()
    server.close()