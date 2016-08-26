import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('localhost', 8001)
sock.connect(serverAddress)
data="{'msgId':'02','sourceId':'0003'}"
if len(data)>100:
 	raise NameError("lenght could not be greater than 99")
data=str(len(data))+data
#data="1"
print data
sock.sendall(data)
