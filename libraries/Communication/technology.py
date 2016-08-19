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
		self.clientList=None												# list of socket,ip. One per ip

	def listen(self):

		while True:
			

		client, clientAddress = self.server.accept() 						# Blocking function. Waits for connections 
		clientList.append([client, clientAddress])


	def receive(self):
		messageLenght =1
		chunks = []
		bytesRecd = 0
		while bytesRecd< messageLenght:
			chunk = client.recv(min(messageLenght - bytesRecd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecd = bytesRecd + len(chunk)
			return ''.join(chunks)

	def send(message, socket):


	# Cleans			

	def addClient():
		clientList

	def printAddress(self):
		print self.clientAddress
