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
link.WiFi.listenConnection()
#print link.WiFi.clientList
#print link.WiFi.clientList[0][0]
aux = link.WiFi.receive(link.WiFi.clientList[0][0])
link.WiFi.send(aux,link.WiFi.clientList[0][0])
link.WiFi.listenConnection()
print link.WiFi.clientList
aux = link.WiFi.receive(link.WiFi.clientList[0][0])
#link.WiFi.send(aux,link.WiFi.clientList[1][0])
print link.WiFi.clientList
#link.aux.printAddress()