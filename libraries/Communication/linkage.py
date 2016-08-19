from technology import *


class Linker:					# if you dont put 'self', variables would be considered gloab names
	def __init__(self):
		self.addresses=[]		# dictionaty with addresses of device vs MAC (WiFi or ZigBee)
		self.technologies=[]	# list with available technologies
		self.lastProtocol=None	# last protocol used for communication
		#self.socket=[]			# list with created sockets
		self.WiFi=WiFi()			# from technology module

	def receive(self):
		return self.aux.receive()


	#def send(self, load, state)
	#	if lastProtocol=='WiFi'
