from technology import *
from random import randint
import os						
import json

class Linker:														# if you dont put 'self', variables would be considered globals
# we assume that messages enter/exist in a dictionary formated state
#	-> parser/deparser for incoming messages
#	-> message contructor. 
	def __init__(self):
		self.connections={}											# dictionary with: {'id':'#','technologyIdentifier':'address'}
		#self.technologies=[]										# list with available technologies
		#self.lastProtocol=None										# last protocol used for communication
		#self.socket=[]												# list with created sockets
		self.TCP=TCP()												# from technology module
		self.technologies={self.TCP.idenfifier:self.TCP}


	#def addConnection(self,id, addressDict)
	#	connectionList[id]=addressDict

	def send(self, id, state):
	# sends state to id using the last used techno.
	# error control if message was not send.
	# to improve:
	# 	-> alternance between technos
	#	-> data constructor
		print '-- link --> sending message'
		data={}
		data['state']=state
		#print data
		data=str(data)
		self.technologies[self.connections[id]['lastTechnology']].send(data,self.connections[id][self.connections[id]['lastTechnology']])

	def receive(self):
	# receives alternating between technos.
	# to add:
	# 	-> control before calling updateConnections().
	#	-> integrity of the message loop control.
	#	-> Just dont like returning three values.
		for techno in self.technologies.itervalues():
			message=techno.receive(1)								# 1 seconds
			if message:
				id=self.updateConnections(message['msgId'],message['sourceId'],message['sourceAddress'],techno.idenfifier)
				#self.send(id,'ON')
				return id, message['state'],message['power']
	
		return None,None,None
		# may we should implement a different function
		# if 
		#auxdict={}
#		if message['msgId']=='01':									# id request from client
#			newId=self.getId()										# por ahora
#			#auxdict=self.connections.get(str(newId))
#			#if auxdict==None:
#			#	auxdict={}
#			auxdict['ip'] = message['sourceAddress']
#			self.connections[str(newId)]=auxdict
#		elif message['msgId']=='02':								# hearbeat
#			if self.connections.has_key(message['senderId']):
#				auxdict=self.connections.get(message['senderId'])	# probably it'll never happens
#			auxdict['ip'] = message['sourceAddress']
#			self.connections[message['senderId']]=auxdict
#		else:
#			raise RuntimeError("wrong msgId") 
		

		
		
		#if self.connections.has_key('001'): print self.connections['001']

	#def send(self, load, state)
	#	if lastProtocol=='WiFi'
	#def receive_test(self):

	#def send(self.message,id):
	# to improve:
	# 	-> error handling: raise error if id is not in the connection list




	def updateConnections(self, msgId, sourceId, sourceAddress, sourceIdentifier):
	# updates connections dictionary. 
	# returns connection's id.
	# to improve:
	#	-> may be it's enough to store the last used techno, deleting the last one even if
	#	it corresponds to another protocol.
		# self.connections=json.dumps({})
		#sourceId=int(sourceId)										# deletes 0's in case of...
		#msgId=int(msgId)											# deletes 0's in case of...
		auxdict={}
		if msgId==1:												# id request from client
			id=self.getId()					
		elif msgId==2:												# heartbeat
			if self.connections.has_key(sourceId):					
				auxdict = self.connections.get(sourceId)			# probably it'll never happens
			id=sourceId
			#auxdict[sourceIdentifier] = sourceAddress
			#self.connections[sourceId] = auxdict
		else:
			raise RuntimeError("wrong msgId")
		auxdict[sourceIdentifier] = sourceAddress
		auxdict['lastTechnology'] = sourceIdentifier				# stores last technology used for reception
		self.connections[id] = auxdict
		#print self.connections
		return id

	#def getId(self):
	#	return randint(0,100)

	def readConnections(self):
		# reads list of connections stored in ./connection_data/connections.json
		# first time it creates both folder and file
		if not os.path.exists('./connection_data/'):
			os.makedirs('./connection_data/')
		file='./connection_data/connections.json'
		#d={'hola':{'chao':'techno'}}
		with open(file, 'a+') as f:									# create file if it not exists
			try: 
				return json.load(f)
			except ValueError:										# reading problems or empty file 
				print 'Could not parse json data.'
			except IOError:											# probably it'll never happens bcse a+
				print 'Could not read file'
			else:													# executes after excepts
				return {}

	def getId(self):
		# read id_history which has the las assigned id
		file='./id_data/id_history.dat'
		id=0	
		if not os.path.exists('./id_data/'):
			os.makedirs('./id_data/')		
		with open(file, 'a+') as f:									# create file if it not exists
			try: 
				id=int(f.readline())
				#print data
			except ValueError:
				print 'Integer error convertion in file id_history.dat:', id
			except IOError:												# probably it'll never happend bcse a+
				print 'Could not read file'
		with open(file, 'w') as f:
			try:
				f.write(str(id+1))								 
			except IOError:
				print 'Could not write file: ', file
		return id+1





