import socket
import sys
import time
import ast
import select
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serverAddress = ('localhost', 9001)
#sock.connect(serverAddress)
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# after interrumping this scripts sockets are still open due to a time_wait state. This cancels it
maxConnections = 10  											
serverAddress=("", 10001)										# defines address and port for the client
server.bind(serverAddress)  								# binds sockets to a specified (address,port) couple
server.listen(maxConnections)




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


inputs = []
outputs = []
connections=[server]
while True:
	print "waiting..."
	readable, writable, exceptional = select.select(connections, outputs,[])
	for s in readable:
		if s is server:										# enters when incoming connection
			print 'incoming connection'
			connection, connection_address = s.accept()
			connections.append(connection)
			connection.setblocking(0)
			#inputs.append(connection)
		else:
			incomingData = getStream(s)
			if incomingData:
				print 'incoming data: ',
				#print "received data"
				print incomingData
			else:
				print 'no incoming data'
				if s in outputs:
					outputs.remove(s)
				connections.remove(s)
				s.close()


#data="{'msgId':1,'sourceId':0,'content':{'prices':1000}}"
#if len(data)>100:
# 	raise NameError("lenght could not be greater than 99")
#data=str(len(data))+data
#while True:
#	tiempo = time.time()
#	sendStream(data,sock)
#	print  getStream(sock)
#	print time.time()-tiempo
#	time.sleep(2)
