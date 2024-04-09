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

def connectDataSock(controlSock):
    dataPort = controlSock.recv(1024).decode()
   
    dataSock = socket(AF_INET, SOCK_STREAM)
    dataSock.connect((server, int(dataPort)))

    return dataSock

# main loop 
while True:
    user_choice = input("ftp> ")
    user_list = user_choice.split()

    if user_choice.startswith("get") and len(user_list) == 2:
        # send data to get file 
        clientSocket.send(user_choice.encode())

        dataSock = connectDataSock(clientSocket)

        fileData = ""                   # buffer to store all data
        fileSize = 0                    # Size of incomming file
        fileSizeBuff = ""               # Buffer with file size

        fileSizeBuff = recvAll(dataSock, 10)        # first 10 bytes contain file size
        

        if fileSizeBuff.count("0") == 10:
            print("File does not exist \n")
            pass
        else:
             fileSize = int(fileSizeBuff)
             print(f"File name is:  {user_choice} \n")
             print(f"File size is {fileSize} \n")

             fileData = recvAll(dataSock, fileSize)     # contains rest of file
             print(f"File data: \n {fileData} \n")


    
    elif user_choice.startswith("ls") and len(user_list) == 1:  # and len(user_choicer) in case user enters ls blah
        clientSocket.send("ls".encode())
        sizeLs = recvAll(clientSocket, 10)
        print(recvAll(clientSocket, int(sizeLs)), "\n")

    elif user_choice.startswith("put") and len(user_list) == 2:
        try:
            filename = user_list[1]

            with open(filename, "rb") as file:
                fileData = file.read()

            clientSocket.send(user_choice.encode())

            fileSize = len(fileData)
            fileSizeStr = str(fileSize).zfill(10)  
            clientSocket.send(fileSizeStr.encode())
            
            print(f"filename: {filename}")
            print(f"number of bytes transferred: {fileSizeStr}")

            clientSocket.sendall(fileData)

            ack = recvAll(clientSocket, 3)
            if ack == "ACK":
                print(f"File '{filename}' sent successfully.")
            else:
                print("Error: Server did not acknowledge the file transfer.")

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error occurred: {e}")

        continue
        
    elif user_choice.startswith("exit"):
        break
    else:
        print("Invalid choice")

print("closing socket")
clientSocket.close()
