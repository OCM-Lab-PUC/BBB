import socket
import ast
import json
#def sendZigBee(self, address,msg):	# address and msg are both strings. Example, address=b'\x00\x13\xA2\x00\x40\xDD\xAA\x83'
#xbee.send('tx', frame_id='A', dest_addr=b'\xFF\xFE', dest_addr_long=address,msg)


# 
#
#
#
#

# Class for TCP socket server connections.
# It stores multiple sockets and constructs a client list.
#
#
# 
class WiFi():

	def __init__(self):
		self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# after interrumping this scripts sockets are still open due to a time_wait state. This cancels it
		self.maxConnections = 5  											
		self.serverAddress=("", 8001)										# defines address and port for the client
		self.server.bind(self.serverAddress)  								# binds sockets to a specified (address,port) couple
		self.server.listen(self.maxConnections)
		self.clients={}														#
		self.idenfifier='WiFi' 												# identifier of the technology.
		#self.server.setblocking(0);
		#print socket.getdefaulttimeout()
	
	# listen incoming client connections, add them to the clientList
	def listenConnection(self):
		client, clientAddress = self.server.accept() 						# Blocking function. Waits for connections... 
		self.clients[clientAddress[0]]=client								# clientAddress=[client_ip, client_port]
		return clientAddress[0]

	def closeConnection(self,socket):
		socket.close()
 
	def receiveFixedLength(self):			
	# receives a message of fixd length
	# timeout not implemented											
		messageLenght = 31													# pre settled lenght. Lose rest of message
		chunks = []
		bytesRecd = 0
		clientIp=self.listenConnection()
		while bytesRecd< messageLenght:
			chunk = self.clients[clientIp].recv(min(messageLenght - bytesRecd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			# Should add parseing unit here

		message=ast.literal_eval(''.join(chunks))							# convert to dictionary
		message['sourceAddress']=clientIp
		#message['content']=''.join(chunks)
		return message

	def receive(self,timeOut):			
	# receives a message of variable length. They are splitted in two parts:
	# "XY" where X is a string of lengtDataLenght bytes whose role is to inform the lenght of actual data
	# Y is the actual data, of lenght dataLenght.
	# to improve:
	# - after accepting connection from client, if no information is received we raise Runtimerror 
	# - if no connection es received, we raise error or return None? I think is better a None						
		dataLenght = 2														 
		lenghtDataLenght = 2												 
		lenghtChunks=[]														# buffer for receiving X
		chunks=[]															# buffer for receiving Y
		bytesRecd = 0
		lenghtBytesRecd=0
		
		
		self.server.settimeout(timeOut)	
		# rises socket.timeout exception after timeOut seconds.

		while True:																# try to encapsulate the following
		# after timeOut seconds of not connections and messages 
		# we stop the listening process and return a None
			try:
				clientIp=self.listenConnection()								# waits for incoming client connection.
				break
			except socket.timeout:
				print "timeout socket"
				return None

		while bytesRecd < dataLenght:
			while lenghtBytesRecd < lenghtDataLenght:
				chunk=self.clients[clientIp].recv(lenghtDataLenght)		 
				if chunk == '':
					raise RuntimeError("socket connection broken")
				lenghtChunks.append(chunk)
				lenghtBytesRecd = lenghtBytesRecd + len(chunk)
				dataLenght=int(''.join(lenghtChunks))
				#if bytesRecd==messageLenght:
				#	print chunks
				#	messageLenght=int(''.join(chunks))
				#	chunks = []
				#	bytesRecd=0
			chunk = self.clients[clientIp].recv(min(dataLenght - bytesRecd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			# Should add parseing unit here
		message=ast.literal_eval(''.join(chunks))						# convert to dictionary
		message['sourceAddress']=clientIp
		#message['content']=''.join(chunks)
		return message



	def send(self, msg):
		totalsent = 0
		while totalsent < len(msg):
			sent = self.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent


	# add pair [socket,ip] to the clientList.
	# does not control if client steals ip.
	# different ips have always different sockets: (server_ip, server_port,client_ip,client_port) is unique			
	def addClient(self, socket, ip):
		notFound=True
		for aux in self.clientList:
			if ip==aux[1]:													# upgrades socket if it was already 			
				aux[0]=socket
				notFound=False
		if notFound:
			self.clientList.append([socket,ip])

	def printAddress(self):
		print self.clientAddress


