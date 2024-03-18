from socket import *
import sys
import subprocess

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
print("Server ready \n")

conn, addy = serverSocket.accept()
print(f"Client connection at socket: {addy[1]} \n")

while True:
    data = conn.recv(3000).decode()

    if data.startswith("get"):
        fileName = data[4:]
        try:
            with open(fileName, "r") as file:
                numSent = 0
                fileData = None

                while True:
                    fileData = file.read(65536)

                    if fileData:
                        size = str(len(fileData))
                        while len(size) < 10:
                            size = "0" + size
                        
                        fileData = size + fileData
                        numSent = 0

                        while len(fileData) > numSent:
                            numSent += conn.send(fileData[numSent:].encode())
                    else:
                        break
            
            print(f"Sent file of size: {size}")
            
        except FileNotFoundError:
            print("File not found")
            noFile = "0" * 10
            conn.send(noFile.encode())
       
       
    elif data.startswith("ls"):
        res = subprocess.getstatusoutput("ls")[1]
        size = str(len(res))
        
        while len(size) < 10:
            size = "0" + size

        conn.send((size + res).encode())

    elif data.startswith("put"):
        try:
            filename = data[4:].strip()

            fileSizeStr = conn.recv(10).decode()
            fileSize = int(fileSizeStr)

            receivedData = b""
            while len(receivedData) < fileSize:
                chunk = conn.recv(65536)
                if not chunk:
                    break
                receivedData += chunk

            with open(filename, "wb") as file:
                file.write(receivedData)

            conn.send("ACK".encode())

            print(f"Received file '{filename}' from client")

        except Exception as e:
            print(f"Error occurred while receiving file: {e}")


    else:
        print(f"Disconnected! at address: {addy}")
        break

serverSocket.close()
        
