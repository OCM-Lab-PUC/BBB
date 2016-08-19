#from DRManagement import EnergyManagement
#casa1=EnergyManagement.HomeEnergyManagementSystem('pablo')
#print casa1.carga.getState()
	#smartplug1=load(10,True)
	#print smartplug1.getState()
	#smartplug1.setState('ON')
	#print smartplug1.getState()
	#print smartplug1.getPower()



from Communication.linkage import *

link=Linker()

print link.clientList()
#link.aux.printAddress()