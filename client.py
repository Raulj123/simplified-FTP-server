from socket import *
import sys

# Retrieve server name and port num
if len(sys.argv) == 3:
    server = sys.argv[1]
    port = int(sys.argv[2])
else:
    sys.exit("Incorrect Format: python client.py <server machine> <server port>")

# TCP socket 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server, port))

