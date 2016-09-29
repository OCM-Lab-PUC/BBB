import socket, select, ast, Queue, errno,time
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
		self.maxConnections = 10  											
		self.serverAddress=("", 8001)										# defines address and port for the client
		self.server.bind(self.serverAddress)  								# binds sockets to a specified (address,port) couple
		self.server.listen(self.maxConnections)
		self.clients={}														# dictionary: {'clientIp':socket}
		self.identifier='TCP' 												# identifier of the technology.
		#self.server.setblocking(0);
		#print socket.getdefaulttimeout()
	
	
	def listenConnection(self):
	# Deprecated
	# listen incoming client connections, add them to the clientList
	# to improve:
	# 	-> Setting time out times must be do in the receive function rather 
	#	than in this one.
		client, clientAddress = self.server.accept() 						# Blocking function. Waits for connections... 
		client.settimeout(2)												# time out for socket.recv() method
		self.clients[clientAddress[0]]=client								# clientAddress=[client_ip, client_port]
		return client, clientAddress[0]										# return  ip address.

	def closeConnections(self):
		for client in self.clients.itervalues():
			client.close()
 
 	def asycSendReceive(self,outQueue,inQueue):

 	# to add:
 	#	-> deparse message routine.
 	#	-> disconection detection.
 	#	-> control if get/sendStream fails or blocks
 	#	-> control if s.accept() fails or blocks
 	#	-> meaning of connection.setblocking(0) is not clear
 	#	-> in linux, if client closes the connections, it arise no key error in data = message_queues[s].get(block=False)
 		inputs = []
		outputs = []
		message_queues = {}
		self.clients['server']=self.server
		
		while True:
			try:
				outgoingData=inQueue.get(block=False)
			except Queue.Empty:
				None
			else:
				connection = self.clients[outgoingData['destinationAddress']]
				if connection not in outputs: 
					outputs.append(connection)
					message_queues[connection] = Queue.Queue()
				message_queues[connection].put(str(outgoingData['content']))
			
			readable, writable, exceptional = select.select(self.clients.values(), outputs, inputs,0)	# if not 0, it blocks it queues are empty
			tiempo=time.time()
			
			for s in writable:
				print time.time()-tiempo
				print "writable "
				try:
					data = message_queues[s].get(block=False)
				except Queue.Empty:
					print "eliminando output"
					outputs.remove(s)
				else:
					print '-- TCP  ---> sending ', data
					self.sendStream(data,s)									
					#s.send(data)
			for s in readable:
				if s is self.server:
					connection, connection_address = s.accept()
					self.clients[connection_address[0]]=connection
					connection.setblocking(0)
					inputs.append(connection)
				else:
					print "leyendo buffer"
					incomingData = self.getStream(s)
					#aux=s.recv(1024)
					#print aux
					#incomingData = ast.literal_eval(aux)
					if incomingData:
						print "received data"
						incomingData['sourceAddress']=self.clients.keys()[self.clients.values().index(s)]	# adding addres of the socket
						outQueue.put(incomingData)
					else:
						print time.time()-tiempo
						print "no data....eliminando"
						inputs.remove(s)									# verificar si es necesario un if
						if s in outputs:
							outputs.remove(s)
						del self.clients[self.clients.keys()[self.clients.values().index(s)]]	# remove s from clients
						s.close()
						if s in message_queues:
							del message_queues[s]

			for s in exceptional:
				print "exceptional"
				inputs.remove(s)
				del self.clients[self.clients.keys()[self.clients.values().index(s)]]
				if s in outputs:
					outputs.remove(s)
				s.close()
				if s in message_queues:
					del message_queues[s]
			#print time.time()-tiempo
			#print "tiempo entero ",time.time()-tiempoentero

	def sendStream(self, data, connection):
		data=str(len(data))+data 
		totalsent = 0
		while totalsent < len(data):
			sent = connection.send(data[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def getStream(self,connection):
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
		#print "Start"
		while bytesRecd < dataLenght:										# reads Y
			while lenghtBytesRecd < lenghtDataLenght:
				try:
					chunk=connection.recv(lenghtDataLenght)					# if no data, returns nothing
					if not chunk:											# catches socket.close()
						return None
					#print chunk
					#print "link: message receive"
				except socket.timeout:
					print "Socket timout"
					return None
				#except socket.error as e:
				#	if e.errno != errno.ECONNRESET:
				#		raise 	# Not error we are looking for
				#	print "socket.error"
				#	return None
					#pass 		# Handle error here.
				else:
					lenghtChunks.append(chunk)
					lenghtBytesRecd = lenghtBytesRecd + len(chunk)
					dataLenght=int(''.join(lenghtChunks))
					#return None

				#if chunk == '':											# from listenConnection()
				#	#print "hola2"
				#	raise RuntimeError("socket connection broken")
				#	return None
				

				#if bytesRecd==messageLenght:
				#	print chunks
				#	messageLenght=int(''.join(chunks))
				#	chunks = []
				#	bytesRecd=0
			#print dataLenght
			try:
				chunk = connection.recv(min(dataLenght - bytesRecd, 2048))	# if no data, return nothing
				if not chunk:
					return None
				#print chunk
			except socket.timeout:
				return None
			else:
				chunks.append(chunk)
				bytesRecd = bytesRecd + len(chunk)
				#print bytesRecd
			#if chunk == '':
				#print "hola4"
				#raise RuntimeError("socket connection broken")
				#return None
			#print "hola5"
		return ast.literal_eval(''.join(chunks))								# joins every into one string
			# Should add parseing unit here


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
	# Deprecated
	# sends message using clients[clientIp] socket to clientIp address.  
		totalsent = 0
		while totalsent < len(msg):
			sent = self.clients[clientIp].send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent


				
	def addClient(self, socket, ip):
	# Deprecated.
	# add pair [socket,ip] to the clientList.
	# does not control if client steals ip.
	# different ips have always different sockets: (server_ip, server_port,client_ip,client_port) is unique
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


