# coding=utf-8
#from linkage import *
from Communication.linkage import *
import time, Queue, random
class Load(object):
	def __init__(self, id, state, power,connected):
		self.state='OFF'										# state of the load, ON OFF
		self.power=power										# power in kW
		self.connected=connected								# TRUE if connection between home and the load is enabled
		self.id=id
		self.commitment=[]
	def __eq__(self, other): 
		if not isinstance(other, Load):
			return False
		return self.id == other.id
	def __hash__(self):
		return 200

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
		self.prices=[]
		self.commitmentMatrix=[]								# commitment matrix (load,state,time). Indicates state of load at time
		self.userPreferences=[]
		self.name=name
		self.link=Linker()
		#self.carga=Load(12,'ON')
		#self.carga.setState('OFF')
		

	def optimize(self):											# Optimizes and modifies commitmentMatrix
		pass

	def main(self):
		set1=set()
		lista1=[]
		carga1=Load(1,'ON','100',True)
		carga2=Load(2,'ON','200',True)
		carga3=Load(3,'ON','200',True)
		set1.add(carga1)
		set1.add(carga2)
		lista1.append(carga1)
		lista1.append(carga2)
		#set2.add(carga1)
		#set2.add(carga3)
		#print carga1==carga2
		#print carga1 in set1

		print hash(carga3)==hash(carga2)
		print carga3==carga2
		print carga3 in {carga2}
		print carga3 in [carga2]
		#print hash(carga3)
		#print hash(carga2)
		#print carga3==carga2
		#print carga3 in set1
		#print carga3 in lista1
		#carga2.id=100
		#for item in Lista1&Lista2:
		#	print item.id

	def informAggregator(self,emissionQueue):
		outMesage={'destinationId':0,'content':{'prices':str(self.prices)}}
		emissionQueue.put(outMesage)
		print '-- HEMS ---> Sending information to aggregator'

	def commit(self,id,emissionQueue):
		lenght=len(self.loads[id].commitment)
		if lenght==0:
			state =0
		elif lenght==1440:
			actualTime=time.localtime().tm_hour*60+time.localtime().tm_min # in minutes
			state=self.loads[id].commitment[actualTime]
		outMesage={'destinationId':id,'content':{'state':state}}
		emissionQueue.put(outMesage)
		print '-- HEMS ---> Sending commmit: load %d, state %d...' % (id,state)


	def updatePrices(self,prices):
		self.prices=prices

	def updateCommitment(self):
		for load in self.loads.itervalues():
			for i in range(1440):
				load.commitment.append(random.randrange(0,2))	# random integer 0 or 1
			#print load.commitment								




	def checkUpdates(self):							
	# Receive messages from loads and aggregator
	# If message comes from a load (id>0) update its state
	# If message comes from the aggregator (id=0) update table of prices
	# after timeOut seconds, clean connected loads
	# to add:
	#	-> message handle for aggregator
	#	-> must tunne up timeOut
	#	-> more encapsulation
	#	-> case handling for (if, msgId) tuple
		timeOut=2.5												# seconds.
		oldLoads=[]												# list for comparing updates in loads 
		receptionQueue=Queue.Queue()
		emissionQueue=Queue.Queue()
		process = threading.Thread(target=self.link.processMessages, args=(receptionQueue,emissionQueue,))
		process.daemon=True
		process.start()

		auxtime = time.time()
		while True:
			try:
				message=receptionQueue.get(block=False)			# we can add a timeOut here
			except Queue.Empty:
				None
			else:
				id, msgId, content= message['sourceId'], message['msgId'], message['content']
				if id>0:										# message from lower level
					if msgId==1:								# heartbeat
						if self.loads.has_key(id):
							self.loads[id].state=content['state']
							self.loads[id].power=content['power']
							self.loads[id].connected=True
						else:
							self.loads[id]=Load(id,content['state'],content['power'],True)
						self.commit(id,emissionQueue)			# send back commitment
				
				elif id==0:											# message from upper level
					if msgId==1:								# prices
						self.updatePrices(content['prices'])
						self.informAggregator(emissionQueue)


				#print 'vacia'
			
			# clean connected loads
			if time.time()-auxtime>timeOut:						# remove every timeOut seconds
				for id in self.loads.keys():
					if self.loads[id].connected:
						self.loads[id].connected=False
					else:	
						del self.loads[id]
				# check for changes in connected loads
				if oldLoads!=self.loads.keys():
					print '-- HEMS ---> Connection/disconnection detected. Updating commitment...' 
					self.updateCommitment()
				oldLoads=self.loads.keys()
				auxtime=time.time()
				print '-- HEMS ---> Connected loads: ',self.loads.keys()

	 

	#def commit():
	#	linker.send(load,state)
	#	return

	#casa1=home()
	#smartplug1=load(10,True)
	#print smartplug1.getState()
	#smartplug1.setState('ON')
	#print smartplug1.getState()
	#print smartplug1.getPower()
