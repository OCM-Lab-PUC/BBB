# coding=utf-8
#from linkage import *
from Communication.linkage import *
import time,Queue
class Load:
	def __init__(self, id, state, power,connected):
		self.state='OFF'										# state of the load, ON OFF
		self.power=power										# power in kW
		self.connected=connected								# TRUE if connection between home and the load is enabled
		self.id=id
	def isConnected(self):
		return connected
	def getState(self):
		return self.state
	def setState(self,state):
		self.state=state
	def getPower(self):
		return self.power
	def setPower(self):
		self.power=power

	# por completar

class HomeEnergyManagementSystem: 								# acá se hace la magia
	## Initializing step: ID,MAC table
	##
	def __init__(self, name):
		self.loads={}											# dictionary of loads= {'id':load}
		self.contracts=[]										# list with contracts
		self.commitmentMatrix=[]								# commitment matrix (load,state,time). Indicates state of load at time
		self.userPreferences=[]
		self.name=name
		self.link=Linker()
		#self.carga=Load(12,'ON')
		#self.carga.setState('OFF')

	def optimize(self):											# Optimizes and modifies commitmentMatrix
		pass
	def update(self):
		pass

	def main(self):
		internalQueue=Queue.Queue()



	def updateLoads(self):							
	# Check for connected loads
	# after timeOut seconds, disconects loads
	# to add:
	#	-> if id=0 for incoming aggregator connection
		internalQueue=Queue.Queue()
		process = threading.Thread(target=self.link.messageProcessing, args=(internalQueue,))
		process.daemon=True
		auxtime = time.time()
		while True:
			
			id, state,power = internalQueue.get()
			#print 'incoming connection from: ',id
			if id:
				self.link.send(id,'ON')
				if self.loads.has_key(id):
					self.loads[id].state=state
					self.loads[id].power=power
					self.loads[id].connected=True
				else:
					self.loads[id]=Load(id,state,power,True)
			#print 'delay: ', time.time()-auxtime
			if time.time()-auxtime>5:							# remove every 5 seconds
				for id in self.loads.keys():
					#print 'updating list of loads...'
					if self.loads[id].connected:
						#print 'load connected: ', id
						self.loads[id].connected=False
					else:
						#print 'removing load: ', id
						del self.loads[id]
				auxtime=time.time()
			print '-- HEMS --> Connected loads: ',self.loads.keys()
	#def commit():
	#	linker.send(load,state)
	#	return

	#casa1=home()
	#smartplug1=load(10,True)
	#print smartplug1.getState()
	#smartplug1.setState('ON')
	#print smartplug1.getState()
	#print smartplug1.getPower()
