# coding=utf-8
class Load:
	def __init__(self, power, connected):
		self.state='OFF'			# state of the load, ON OFF
		self.power=power			# power in kW
		self.connected=connected	# TRUE if connection between home and the load is enabled
	def isConnected(self):
		return connected
	def getState(self):
		return self.state
	def setState(self,state):
		self.state=state
	def getPower(self):
		return self.power
	# por completar

class HomeEnergyManagementSystem: # acá se hace la magia
	## Initializing step: ID,MAC table
	##
	def __init__(self, name):
		self.loads=[]				# list with the loads actually connected to home. 
		self.contracts=[]			# list with contracts
		self.commitmentMatrix=[]	# commitment matrix (load,state,time). Indicates state of load at time
		self.userPreferences=[]
		self.name=name
		#self.carga=Load(12,'ON')
		#self.carga.setState('OFF')

	def optimize():				# Optimizes and modifies commitmentMatrix
		pass

	def check():					# Check for updates in loads, contracts and user preferences
		pass
	#def commit():
	#	linker.send(load,state)
	#	return

	#casa1=home()
	#smartplug1=load(10,True)
	#print smartplug1.getState()
	#smartplug1.setState('ON')
	#print smartplug1.getState()
	#print smartplug1.getPower()
