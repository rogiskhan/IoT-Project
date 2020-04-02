
from telegram import * #mia classe
import time 
from gpiozero import Button, RGBLED, Buzzer
from colorzero import Color #serve per i colori del led

#manca il buzzer e il led come metodi
class notifier(object):
	def __init__(self, pin, token, pinbuzzer, pinr, ping, pinb):#inizializzazione GPIO e comunicazione con il bot di telegram
		self.rgb_led = RGBLED(pinr, ping, pinb, pwm = True)#istanzio il led
		self.button=Button(pin, bounce_time=100, pull_up=False)#istanzio il pulsante
		self.buzzer=Buzzer(pinbuzzer)#istanzio il buzzer
		self.tg=telegram(token)#istanzion telegram
		self.pushed=0 #setto a zero una variabile per il loop e la callback
		self.rgb_led.value = Color('green') #metot il led verd, questa è la prima funzione che viene eseguita all'avvio del pacchetto
		self.tg.starting_loop()  #cerco il messaggio start all'avvio dell'applicazione. Va messo in init perché va tutto inizializzato all'avvio del sistema

	def my_callback(self):  #callback pulsante premuto
		
		self.pushed=1
	   	self.rgb_led.value = Color('green')#quando ha preso il medicinale metto il colore verde
#crit è una soglia di messaggio entro cui devo mandare la notifica speciale col buzzer
	def message_loop(self, msg, freq, crit):#freq è ogni quanto mando il messaggio sarebbe scorretto ma è più intuitivo espresso in minuti
		self.rgb_led.value = Color('magenta')#colore di qunado va presa la pillola
		self.button.when_pressed=self.my_callback #interrupt del pulsante
		start=time.time()#inizio il conto del ritardo
		count=0#inizio il conteggio dei messaggi
		while self.pushed==0:#loop di invio del messaggio
			self.tg.send_update(msg)
			count=count+1	
			if count>crit:#se sto nel crit avvio led rosso e buzzer
				self.buzzer_sound(freq*60)
				self.rgb_led.value = Color('red')
			for i in range(int(freq*60)):#polling per il conteggio del tempo tra un messaggio e l'altro
				if self.pushed==0:
					time.sleep(1)
				else:
					break
		end=time.time()#ha premo il pulsante sono fuori dal loop finisco il conteggio del ritardo
		if count>1: #solo se l'utente si fa pregare considero il ritardo
			dt=end-start#ritardo
			m, s = divmod(dt, 60)#conversione in minuti e secondi
			prompt=(f'Sei in ritardo di {int(m)} minuti e {int(s)} secondi!')
			self.tg.send_update(prompt)
			return dt
		else:
			dt=0#se ho mandato solo un messaggio considero la cosa buona e conto ritardo nullo
			return dt
	  
	def buzzer_sound(self,tim):#tim è il tempo che il buzzer suona
		periodo=int(tim/1)#lascio 1 perché mi ricordo che divido per la somma del tempo on e off
		self.buzzer.beep(on_time=0.5, off_time=0.5, n=periodo, background=True)

	def switch(self, score, orario):
		scor=score[orario]
		if scor<2:
			f=20 #frequenza dei messaggi
			crit=1000 #infinito

		elif scor<5:
			f=15
			crit=2#dopo il terzo messaggio
		elif scor<7:
			f=10
			crit=2

		elif scor<=10:
			f=7
			crit=2

		return f, crit




if __name__ == '__main__':
	pin=22
	buzzer=23
	token='495943086:AAFzwh0IU9bmKXNL4cAoPa2he7BmLuLhPhU' #token di un bot provvisiorio mio a breve ne metteremo un altro
	msg='Ciao sono lollo barcollo ma non mollo' #simulazione del messagio da mandare
	f=0.5 #periodo di invio dovrebbe essere un output della funzione
	no=notifier(pin,token, buzzer, 18, 17, 27)
	no.message_loop(msg, f, 1)