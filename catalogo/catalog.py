import cherrypy
import json 
import time
class Catalog(object):
  def __init__(self):
    self.services={} #{"serial":[devices], serial:[devices]} dove ogni device è un dizionario
    self.actualTime=time.time()
    self.catalogo={"updated":""} #catalogo= {"updated": 3442, "serial1": {{}, {}, ecc}
 
  def addID(self,serial_number):
    print(serial_number)
    #self.devices =[]
    self.services.update({serial_number:[]})
    self.catalogo[serial_number]={"services":self.services[serial_number]}
  def addService(self,servicesInfo):
    for serial in self.services.keys():
      if serial==servicesInfo["serial_number"]:
        self.services[serial].append(servicesInfo)
        self.catalogo[serial]["services"] = self.services[serial]
        self.actualTime=time.time()
  def updateService(self,serviceID,servicesInfo):
    for serial in self.services.keys():
      if serial==servicesInfo["serial_number"]:
        for i in range(len(self.services[serial])):
          service=self.services[serial][i]
          if service["ID"]==serviceID:
            self.services[serial][i]=servicesInfo
      self.actualTime=time.time()
  def removeDevices(self,serial): #per rimuovere "manualmente"
    for key in self.services.keys():
        if key == serial:
          self.services.pop(key)
          self.catalogo.pop(key)
    
          print(f'device with serial number {key} has been removed ')
          self.actualTime=time.time()
          break
  def removeInactive(self):
    print("sto vivendo")
    now = time.time()
    for serial in self.services.keys():
      for i in range(len(self.services[serial])):
        service=self.services[serial][i]
        if now - (service["last_update"])>10:
          self.services[serial].pop(i)
          print(f'service with ID {service["ID"]} and serial number {serial} has been removed ')
          self.actualTime=time.time()
          break
       
class CatalogREST(object):
  exposed=True
  def __init__(self,clientID):
    self.ID=clientID
    self.catalog=Catalog()
  def GET(self,*uri,**params):
    if len(uri)==0:
      print("seees")
      self.catalog.catalogo["updated"] = self.catalog.actualTime
      output=self.catalog.catalogo
     
    else:
      output={"services":self.catalog.catalogo[uri[0]]["services"]}
    return json.dumps(output)
  def PUT(self,**params):
    body=cherrypy.request.body.read()
    json_body=json.loads(body)

    for b in json_body:
        if not any(d == b["serial_number"] for d in self.catalog.services.keys()):
          self.catalog.addID(b["serial_number"])
        if not any(d['ID']== b["ID"] for d in self.catalog.services[b["serial_number"]]):
          last_update=time.time()
          b['last_update']=last_update
          
          #self.catalog.addID(b['serial_number'])
          self.catalog.addService(b)
          output=f'Service with ID {b["ID"]}, serial number {b["serial_number"]}has been added'
          print (output)
          return output
        else:

          last_update=time.time()
          b["last_update"]=last_update
          self.catalog.updateService(b['ID'],b)
    
    #print(body)
    return body
#questo serve per eliminare il service manualmente
  def DELETE(self,*uri):
    #for device in self.catalog.catalogo[uri[0]]:#uri[0] è serial number
    self.catalog.removeDevices(uri[0]) #
    output=f"Device and serial {uri[0]} has been removed"
    return output


     # creo il catalogo
if __name__=="__main__":    
    catalogClient = CatalogREST('Catalog')
    

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.tree.mount(catalogClient, '/', conf)
    cherrypy.engine.start()
    
    while True:
        catalogClient.catalog.removeInactive()
        time.sleep(5)
    cherrypy.engine.exit()
  