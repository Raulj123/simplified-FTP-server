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

# funtion to avoid overflow 
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff = sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff.decode()
	
	return recvBuff



# main loop 
while True:
    user_choice = input("ftp> ")
    user_list = user_choice.split()

    if user_choice.startswith("get") and len(user_list) == 2:
        # send data to get file 
        clientSocket.send(user_choice.encode())

        fileData = ""                   # buffer to store all data
        fileSize = 0                    # Size of incomming file
        fileSizeBuff = ""               # Buffer with file size

        fileSizeBuff = recvAll(clientSocket, 10)        # first 10 bytes contain file size
        
        if fileSizeBuff.count("0") == 10:
             print("File does not exist \n")
        else:
             fileSize = int(fileSizeBuff)
             print(f"File size is {fileSize} \n")

             fileData = recvAll(clientSocket, fileSize)     # contains rest of file
             print(f"File data: \n {fileData} \n")


    
    elif user_choice.startswith("ls"):
        clientSocket.send("ls".encode())

    elif user_choice.startswith("put"):
        clientSocket.send(user_choice.encode())

    elif user_choice.startswith("exit"):
        break
    else:
        print("Invalid choice")

print("closing socket")
clientSocket.close()