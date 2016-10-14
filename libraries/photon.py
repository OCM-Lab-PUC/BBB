import socket
import sys
import time
import ast
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('localhost', 8001)
sock.connect(serverAddress)
#sock.setblocking(0)
def sendStream(data, connection): 
	totalsent = 0
	while totalsent < len(data):
		sent = connection.send(data[totalsent:])
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent

def getStream(connection):
		dataLenght = 2														 
		lenghtDataLenght = 2												 
		lenghtChunks=[]														# buffer for receiving X
		chunks=[]															# buffer for receiving Y
		bytesRecd = 0
		lenghtBytesRecd=0
		while bytesRecd < dataLenght:										# reads Y
			while lenghtBytesRecd < lenghtDataLenght:
				try:
					chunk=connection.recv(lenghtDataLenght)					# may be we should get directly the socket \\
				except socket.timeout:
					return None
				lenghtChunks.append(chunk)
				lenghtBytesRecd = lenghtBytesRecd + len(chunk)
				dataLenght=int(''.join(lenghtChunks))
			try:
				chunk = connection.recv(min(dataLenght - bytesRecd, 2048))
			except socket.timeout:
				return None
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
		return ast.literal_eval(''.join(chunks))								# joins every into one string


data="{'msgId':1,'sourceId':8,'content':{'power':100,'state':0}}"
#print data
#print len(data)
if len(data)>100:
 	raise NameError("lenght could not be greater than 99")
data=str(len(data))+data

#data=""
#print data
#sock.sendall(data)
#time.sleep(3)
while True:
	tiempo = time.time()
	sendStream(data,sock)
	print  getStream(sock)
	print time.time()-tiempo
	time.sleep(2)
#time.sleep(1)
#sock.close()
#while True:
#	time.sleep(1)
#time.sleep(5)
#sock.close()
#time.sleep(5)
#print 'state:', getStream(sock)
#sock.close()
