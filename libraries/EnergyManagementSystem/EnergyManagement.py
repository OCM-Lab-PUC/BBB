from Actors import *

def HomeEnergyManagement():	# acá se hace la magia
	## Initializing step: ID,MAC table

	##
	casa1=home()
	smartplug1=load(10,True)
	print smartplug1.getState()
	smartplug1.setState('ON')
	print smartplug1.getState()
	print smartplug1.getPower()
