# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:14:48 2020

@author: monal
"""

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
    if not any(d['ID']==json_body['ID'] for d in self.catalog.devices):
      last_update=time.time()
      json_body['last_update']=last_update
      self.catalog.addDevice(json_body)
      output=f"Device with ID {json_body['ID']} has been added"
      print (output)
      return output
    else:
      last_update=time.time()
      json_body['last_update']=last_update
      self.catalog.updateDevice(json_body['ID'],json_body)
      print("trovato")
    print(body)
    return body

  def DELETE(self,*uri):
    self.catalog.removeDevices(uri[0])
    output=f"Device with ID {uri[0]} has been removed"
    print (output)


if __name__ == '__main__':
  catalogClient=CatalogREST('Catalog')
  conf={
    '/':{
        'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
        'tool.session.on':True
    }
  }
  cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 80})
  cherrypy.tree.mount(catalogClient,'/',conf)
  cherrypy.engine.start()

  while True:
    catalogClient.catalog.removeInactive()
    with open("output.json", "w") as f:
      json.dump(catalogClient.catalog.devices, f)
    time.sleep(5)
  cherrypy.engine.exit()
  