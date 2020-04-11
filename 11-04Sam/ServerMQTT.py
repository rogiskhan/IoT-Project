

###sottoclasse di MyMQTT per gestire il server

from MyMQTT import *
from Comunic_ThingSpeak import *
import json

class ServerMQTT(MyMQTT):
	def __init__(self, clientID, broker):
		MyMQTT.__init__(self, clientID, broker)

		
		self.c=Comunic_ThingSpeak(channelID, apiKey) #istanzio l'oggetto thingspeak
		#istanzio le variabili di cui ho bisogno qua. Nel main verranno comunque richiamate
		self.piano={} #qui si mette il piano
		self.index=0 #l'indice che mi dice a quale punto sono arrivato
		self.chiavi=[] #lista contenente gli orari
		self.ritardi={} #dizionario con i ritardi. Struttura ritardi={str_ora:ritardo}
		self.ritm=0 #ritardo massimo (prossima_ora-ora_attuale)
		self._paho_mqtt.on_message = self.myOnMessageReceived

	def myOnMessageReceived(self, paho_mqtt , userdata, msg):
		###interrupt di ricezione dei messaggi###
		if msg.topic=='nomeutente/ritardi': #arrivano i ritardi dopo che il pulsante è stato premuto/è scaduto il tempo
			data=json.loads(msg.payload)
			
			rit=data['ritardo']
			#prendo il valore dal dizionario e aggiorno il dizionario dei ritardi
			self.ritardi.update({self.chiavi[self.index]:rit})
			#l'if indica se si è scordato o meno serve poi su thingspeak per stampare o meno questo dato
			if self.ritm-rit==0:
				
				self.c.send_ts(self.chiavi[self.index], str(self.piano[self.chiavi[self.index]])[2:-2], rit, 0) #mando i dati a thingspeak se non è preso

			else:
	
				self.c.send_ts(self.chiavi[self.index], str(self.piano[self.chiavi[self.index]])[2:-2], rit)
			#aumento l'indice perché so che la notifica è arrivata e uso il ritardo come feedback
			self.index=self.index+1
			#controllo se è l'ultima medicina della giornata. Se lo è resetto l'indice a 0 e si ricomincia la routine
			if self.index>(len(self.chiavi)-1):
			
				self.index=0

			#mando allo schermo i datida stampare per la prossima medicina
			self.myPublish('nomeutente/prox', json.dumps({'medicine': self.piano[self.chiavi[self.index]], 'orario':self.chiavi[self.index]})) #da mandare per il display
			



		elif msg.topic=='nomeutente/piano':
			#quando arriva un nuovo piano

			data=json.loads(msg.payload)
			
			self.piano=data['piano']
			

