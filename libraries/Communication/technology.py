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
class TCP():

	def __init__(self):
		self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# after interrumping this scripts sockets are still open due to a time_wait state. This cancels it
		self.maxConnections = 5  											
		self.serverAddress=("", 8001)										# defines address and port for the client
		self.server.bind(self.serverAddress)  								# binds sockets to a specified (address,port) couple
		self.server.listen(self.maxConnections)
		self.clients={}														# dictionary: {'clientIp':socket}
		self.idenfifier='TCP' 												# identifier of the technology.
		#self.server.setblocking(0);
		#print socket.getdefaulttimeout()
	
	# listen incoming client connections, add them to the clientList
	def listenConnection(self):
	# to improve:
	# 	-> Setting time out times must be do in the receive function rather 
	#	than in this one.
		client, clientAddress = self.server.accept() 						# Blocking function. Waits for connections... 
		client.settimeout(2)												# time out for socket.recv() method
		self.clients[clientAddress[0]]=client								# clientAddress=[client_ip, client_port]
		return client, clientAddress[0]												# return  ip address.

	def closeConnections(self):
		for client in self.clients.itervalues():
			client.close()
 
#	def receiveFixedLength(self):			
#	# receives a message of fixed length
#	# timeout not implemented											
#		messageLenght = 31													# pre settled lenght. Loses rest of message
#		chunks = []
#		bytesRecd = 0
#		clientIp=self.listenConnection()
#		while bytesRecd< messageLenght:
#			chunk = self.clients[clientIp].recv(min(messageLenght - bytesRecd, 2048))
#			if chunk == '':
#				raise RuntimeError("socket connection broken")
#			chunks.append(chunk)
#			bytesRecd = bytesRecd + len(chunk)
#			# Should add parseing unit here#

#		message=ast.literal_eval(''.join(chunks))							# convert to dictionary
#		message['sourceAddress']=clientIp
#		#message['content']=''.join(chunks)
#		return message

	def receive(self,timeOut):			
	# receives a message of variable length. They are splitted in two parts:
	# "XY" where X is a string of lenghtDataLenght bytes whose role is to 
	# inform the lenght of actual data Y of lenght dataLenght.
	# to improve:
	#	-> socket.recv and socket.liste have both a waiting time (time out). 
	#	Both times must be tunned up.
	#	-> no event handling for incoming null messages.
	#	-> socket must be closed after calling socket.recev(). This makes 
	#	that incoming messages from already opened connections will not arrive.
		dataLenght = 2														 
		lenghtDataLenght = 2												 
		lenghtChunks=[]														# buffer for receiving X
		chunks=[]															# buffer for receiving Y
		bytesRecd = 0
		lenghtBytesRecd=0
		
		self.server.settimeout(timeOut)										# rises socket.timeout exception 

		while True:															# try to encapsulate the following
		# returns None after timeOut of incoming connections
			try:
				client, clientAddress=self.listenConnection()				# waits for incoming client connection.
				break
			except socket.timeout:
				#print "timeout socket"
				return None
		# return None if no message is readed or lenghts mismatch
		while bytesRecd < dataLenght:										# reads Y
			while lenghtBytesRecd < lenghtDataLenght:
				#print "link: receving message"
				try:
					chunk=client.recv(lenghtDataLenght)						# may we should get directly the socket \\
					#print "link: message receive"
				except socket.timeout:
					return None
				#if chunk == '':											# from listenConnection()
				#	#print "hola2"
				#	raise RuntimeError("socket connection broken")
				#	return None
				
				lenghtChunks.append(chunk)
				lenghtBytesRecd = lenghtBytesRecd + len(chunk)
				dataLenght=int(''.join(lenghtChunks))
				#if bytesRecd==messageLenght:
				#	print chunks
				#	messageLenght=int(''.join(chunks))
				#	chunks = []
				#	bytesRecd=0
			try:
				chunk = client.recv(min(dataLenght - bytesRecd, 2048))
			except socket.timeout:
				return None

			#if chunk == '':
				#print "hola4"
				#raise RuntimeError("socket connection broken")
				#return None
			#print "hola5"
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			# Should add parseing unit here
		message=ast.literal_eval(''.join(chunks))							# convert to dictionary
		print '-- TCP ---> ', clientAddress
		message['sourceAddress']=clientAddress
		#message['content']=''.join(chunks)
		return message



	def send(self, msg, clientIp):
	# sends message using clients[clientIp] socket to clientIp address.  
		totalsent = 0
		while totalsent < len(msg):
			sent = self.clients[clientIp].send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent


	# add pair [socket,ip] to the clientList.
	# does not control if client steals ip.
	# different ips have always different sockets: (server_ip, server_port,client_ip,client_port) is unique			
	def addClient(self, socket, ip):
	# to improve
	#	-> close unused sockets.
		notFound=True
		for aux in self.clientList:
			if ip==aux[1]:													# upgrades socket if it was already 			
				aux[0]=socket
				notFound=False
		if notFound:
			self.clientList.append([socket,ip])

	def printAddress(self):
		print self.clientAddress


