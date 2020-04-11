
###sottoclasse di MyMQTT per gestire il device

#praticamente il dispositivo lavora quasi solo in interrupt quindi è quasi tutto qua

from MyMQTT import *
from notifier import *
from display import *
import json

class DeviceMQTT(MyMQTT):
	def __init__(self, clientID, broker):
		#inizializzazione dell'hardware e dei dati
		self.clientID=clientID
		self.broker=broker
		MyMQTT.__init__(self, self.clientID, self.broker)
		pin=22
		token='495943086:AAFzwh0IU9bmKXNL4cAoPa2he7BmLuLhPhU' #token di un bot provvisiorio mio a breve ne metteremo un altro
		buzzer=23
		pinr=18
		ping=17
		pinb=27
		self.d=display()
		#messaggio di inizializzazione
		self.d.print_init()
		self.no=notifier(pin, token, buzzer, pinr, ping, pinb)
		#sistemando la parte del display qua dovrei printare il fatto che ora l'utente deve inserire il piano
		self._paho_mqtt.on_message = self.myOnMessageReceived

	def myOnMessageReceived(self, paho_mqtt , userdata, msg):
		###gestione messaggi in mqtt in interrupt
		
		
		if msg.topic=='nomeutente/prox':
			
			#ricevo orario e medicine che stanno per essere prese e le printo
			data=json.loads(msg.payload)
			
			ora=data['orario']
			medicine=data['medicine']


			self.d.print_med(ora, medicine) #stampo il prossimo "appuntamento"

		elif msg.topic=='nomeutente/notific':

			data=json.loads(msg.payload)
			#ricevo l'interrupt per mandare il messaggio
			msg=data['messaggio']
			f=data['frequenza']
			crit=data['n_msg_critici']
			ritm=data['ritardo_massimo']
			rit=self.no.message_loop(msg, f, crit, ritm)
			#mando indietro il ritardo
			self.myPublish('nomeutente/ritardi', json.dumps({'ritardo':rit}))