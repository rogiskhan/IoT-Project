import cherrypy
import json 
import time
class Catalog(object):
  def __init__(self):
    self.devices=[]
    self.actualTime=time.time()
  def addDevice(self,devicesInfo):
    self.devices.append(devicesInfo)
  def updateDevice(self,deviceID,devicesInfo):
    for i in range(len(self.devices)):
      device=self.devices[i]
      if device['ID']==deviceID:
        self.devices[i]=devicesInfo
  def removeDevices(self,deviceID):
    for i in range(len(self.devices)):
      device=self.devices[i]
      if device['ID']==deviceID:
        self.devices.pop(i)
  def removeInactive(self):
    self.actualTime=time.time()
    for device in self.devices:
      if self.actualTime-device['last_update']>10:
        self.devices.remove(device)

class CatalogREST(object):
  exposed=True
  def __init__(self,clientID):
    self.ID=clientID
    self.catalog=Catalog()
  def GET(self,*uri,**params):
    output={'devices':self.catalog.devices,"updated":self.catalog.actualTime}
    return json.dumps(output)
  def PUT(self,**params):
    body=cherrypy.request.body.read()
    json_body=json.loads(body)
    for b in json_body:
        if not any(d['ID']== b["ID"] for d in self.catalog.devices):
          last_update=time.time()
          b['last_update']=last_update
          self.catalog.addDevice(b)
          output=f"Device with ID {b['ID']} has been added"
          print (output)
          return output
        else:
          last_update=time.time()
          b['last_update']=last_update
          self.catalog.updateDevice(b['ID'],b)
          print("trovato")
    #print(body)
    return body

  def DELETE(self,*uri):
    self.catalog.removeDevices(uri[0])
    output=f"Device with ID {uri[0]} has been removed"
    print (output)


