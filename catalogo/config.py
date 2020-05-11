import json

class Config():
  def getserial(self):
    # Extract serial from cpuinfo file
    self.cpuserial = "0000000000000000"
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line[0:6]=='Serial':
          self.cpuserial = line[10:26]
      f.close()
    except:
      self.cpuserial = "ERROR000000000"
    return self.cpuserial
  def log(self):
    file= open('device_settings.json','w')
    dic={"clientID": "Device_"+self.cpuserial, "broker": "mqtt.eclipse.org", "ID": "ID" , "pin_button": 22, "pin_buzzer": 23, "pin_red": 18, "pin_green": 17, "pin_blue": 27, "token": "1106290892:AAH88UcA5oBxqsyS3tePDA0qniWquJi6_XE", "bot": "@PortaPilloleIoTbot",
    "serial_number":self.cpuserial}
    json.dump(dic,file)