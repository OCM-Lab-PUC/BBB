import socket

#def sendZigBee(self, address,msg):	# address and msg are both strings. Example, address=b'\x00\x13\xA2\x00\x40\xDD\xAA\x83'
#xbee.send('tx', frame_id='A', dest_addr=b'\xFF\xFE', dest_addr_long=address,msg)


# 
#
#
#
#


class WiFi:

	def __init__(self):
		self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# after interrumping this scripts sockets are still open due to a time_wait state. This cancels it
		self.maxConnections = 5  											
		self.serverAddress=("", 8001)										# defines port
		self.server.bind(self.serverAddress)  								# binds sockets to a specified address
		self.server.listen(self.maxConnections)
		self.clientList=[]													# list of [socket,ip]. One per ip

	def listenConnection(self):
		client, clientAddress = self.server.accept() 						# Blocking function. Waits for connections 
		self.addClient(client,clientAddress[0])					
		return True

	def closeConnection(self,socket):
		socket.close()

	def receive(self,socket):														
		messageLenght =1
		chunks = []
		bytesRecd = 0
		while bytesRecd< messageLenght:
			chunk = socket.recv(min(messageLenght - bytesRecd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			return ''.join(chunks)

	def send(self, message, socket):
		totalsent = 0
		while totalsent < len(message):
			sent = socket.send(message[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent


	# Cleans			
	def addClient(self, socket, ip):
		notFound=True
		for aux in self.clientList:
			if ip==aux[1]:
				aux[0]=socket
				notFound=False
		if notFound:
			self.clientList.append([socket,ip])



	def printAddress(self):
		print self.clientAddress
