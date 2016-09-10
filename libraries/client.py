import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('localhost', 8001)
sock.connect(serverAddress)


def receiveFixedLength(self):			
	# receives a message of fixed length
	# timeout not implemented
	# to check:
	#	-> contrary to servers, when client reads de reception buffer
	#	gives '' 											
		messageLenght = 15													# pre settled lenght. Loses rest of message
		chunks = []
		bytesRecd = 0
		#clientIp=self.listenConnection()
		while bytesRecd< messageLenght:
			chunk = self.recv(min(messageLenght - bytesRecd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			# Should add parseing unit here

		message=''.join(chunks)
		#message['sourceAddress']=clientIp
		#message['content']=''.join(chunks)
		return message

data="{'msgId':2,'sourceId':5,'power':100,'state':0}"
if len(data)>100:
 	raise NameError("lenght could not be greater than 99")
data=str(len(data))+data
#data=""
print data
sock.sendall(data)
print 'state:', receiveFixedLength(sock)
sock.close()
