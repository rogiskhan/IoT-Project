###sottoclasse di MyMQTT per gestire il device

#praticamente il dispositivo lavora quasi solo in interrupt quindi è quasi tutto qua

from MyMQTT import *
from notifier import *
from display import *
import json
from numpy import random
from subprocess import call



class DeviceMQTT(MyMQTT):
	def __init__(self):
		#inizializzazione dell'hardware e dei dati
		#settings
		with open("device_log.JSON", "r") as f:
			settings = json.load(f)
		#ho spostato tutto dentro alla fine perché effettivamente così apro una volta sola
		#robe per la notifica
		pin_button = settings["pin_button"]
		pin_buzzer = settings["pin_buzzer"]
		pin_red = settings["pin_red"]
		pin_green = settings["pin_green"]
		pin_blue = settings["pin_blue"]
		token = settings["token"]
		bot=settings["bot"]
		#dati per mqtt
		clientID = settings["clientID"]
		broker = settings["broker"]
		self.piano={}
		#dati sui topic
		self.topic1 = settings["ID"] + '/ritardi'
		self.topic2 = settings["ID"] + '/prox'
		self.topic3 = settings["ID"] + '/notific'
		
		MyMQTT.__init__(self, clientID, broker)

		self.d=display()
		print('display ok')

		#messaggio di inizializzazione
		txt_b=f"Scrivi start al bot telegram {bot}"
		self.d.print_display('Benvenuto. Sto inizializzando...', txt_b)
		
		self.no=notifier(pin_button, token, pin_buzzer, pin_red, pin_green, pin_blue)
		#sistemando la parte del display qua dovrei printare il fatto che ora l'utente deve inserire il piano
		txt_b="Ora connettiti alla pagina e inserisci il piano"
		txt_y="Quasi finito..."
		self.d.print_display(txt_y, txt_b)
		self._paho_mqtt.on_message = self.myOnMessageReceived

	def myOnMessageReceived(self, paho_mqtt , userdata, msg):
		###gestione messaggi in mqtt in interrupt
		
		
		if msg.topic==self.topic2:
			
			#ricevo orario e medicine che stanno per essere prese e le printo
			data=json.loads(msg.payload)
			print(data)
			self.ora=data['orario']
			self.medicine=data['medicine']
			self.piano=data['piano']
			txt_y=f'Prossima medicina: {self.ora}'
			#occhio che sicuramente sto join fa più danni della grandine
			txt_b=", ".join(self.medicine)
			
			self.d.print_display(txt_y, txt_b)
			#stampo il prossimo "appuntamento"

		elif msg.topic==self.topic3:

			data=json.loads(msg.payload)
			#ricevo l'interrupt per mandare il messaggio
			print(data)
			msg=data['messaggio']
			f=data['frequenza']
			crit=data['n_msg_critici']
			ritm=data['ritardo_massimo']

			self.ora=data['orario']
			self.medicine=data['medicine']
			txt_y=f'Sono le {self.ora}. È ora!'
			txt_b=", ".join(self.medicine)
			self.d.print_display(txt_y, txt_b)

			rit=self.no.message_loop(msg, f, crit, ritm)
			#mando indietro il ritardo
			self.myPublish(self.topic1, json.dumps({'ritardo':rit}))

			#posizione brutta ma non so dove metterla. Funzione per spegnere


	def waiting_msg(self):
		while True:
			comando=self.no.tg.waiting()
			if comando=='S':
				self.d.print_logo()
				self.d.close_all()
				call("sudo poweroff", shell=True)
			elif comando=='P':
				#rispondi con il piano
				if self.piano=={}:
					self.no.tg.send_update('Non hai inserito il piano')
					

					
				else:
					self.no.tg.send_update(str(self.piano))
					
			elif comando=='C':
				#rispondi con consigli a caso
				with open("tips.JSON", "r") as f:
					consigli = json.load(f) #apro una lista di consigli
				consiglio=random.randint(0, len(consigli)-1)
				self.no.tg.send_update(consigli[consiglio])
			
			comando=None
			