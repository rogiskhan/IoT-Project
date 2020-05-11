from threading import Timer, Thread, Event
import json
import time
import requests 
#c lasse per gestire altre funzioni con il timer se devo passare parametri vanno messi come parametri globali della classe
class perpetualTimer():

   def __init__(self, t, hFunction, params=None):
      self.params = params
      self.t = t
      self.hFunction = hFunction
      self.thread = Timer(self.t, self.handle_function)
       # class Timer: prendeem in ingresso il tempo(in secondi) e la funzione che
       # deve essere eseguita dopo quel tpo
   def handle_function(self):
      if self.params == None:
         self.hFunction()
      else:
         self.hFunction(self.params)
      self.thread = Timer(self.t, self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()   
def send_get(body):
  with open("device_settings.json", "r") as f:
      settings = json.load(f)

  serialnumber=body[0]['serial_number']

  r1=requests.put('http://127.0.0.1:8080',data = json.dumps(body))
  time.sleep(10)
  r2=requests.get('http://127.0.0.1:8080/'+serialnumber) #+serialnumber
  #print(r2.json())

