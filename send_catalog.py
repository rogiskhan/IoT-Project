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
def send(serviceID):
    requests.put("http://localhost",data = json.dumps(serviceID))


t = perpetualTimer(5,send,{'ID':12})
t1 = perpetualTimer(5,send,{'ID':14})
t.start()
t1.start()