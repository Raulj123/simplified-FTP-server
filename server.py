from socket import *
import sys

# Retrieve port num
if len(sys.argv) == 2:
    if sys.argv[1].isnumeric():
        port = int(sys.argv[1])
    else:
        sys.exit(f"Port number must be numeric. Received: {sys.argv[1]}")
else:
    sys.exit("Incorrect Format: python client.py <server machine> <server port>")

# TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(5)
print("Server ready")

conn, addy = serverSocket.accept()
print(f"Client connection at socket: {addy[1]}")