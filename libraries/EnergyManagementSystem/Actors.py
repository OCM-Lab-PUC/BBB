class load:
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

class home:
	def __init__(self):
		self.loads=[]				# list with the loads actually connected to home. 
		self.contracts=[]			# list with contracts
		self.commitmentMatrix=[]	# commitment matrix (load,state,time). Indicates state of load at time
		self.userPreferences=[]

	def optimize():				# Optimizes and modifies commitmentMatrix
		return

	def check():					# Check for updates in loads, contracts and user preferences
		return True


