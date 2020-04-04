from display import *
from notifier import *
from Comunic_ThingSpeak import *
from dati import *
import time
import json
##questo è il main
#prima fase: si inizializza
if __name__ == '__main__':
	#setup
	d=display()
	pin=22
	token='495943086:AAFzwh0IU9bmKXNL4cAoPa2he7BmLuLhPhU' #token di un bot provvisiorio mio a breve ne metteremo un altro
	buzzer=23
	pinr=18
	ping=17
	pinb=27
	print('in')
	d.print_init()
	no=notifier(pin, token, buzzer, pinr, ping, pinb)
	c=Comunic_ThingSpeak()
	dati=dati()

	#simula in database
	farmaci={
	   'vivinC':{
	   'pericolosità': 1,
	   'principio attivo': 'Boh',
	   'dose': 100,
	   'interazione': None
	   },
	   'aspirina':{
	   'pericolosità': 3,
	   'principio attivo': 'Boh',
	   'dose': 100,
	   'interazione': None
	   },
	   'tachipirina':{
	   'pericolosità': 6,
	   'principio attivo': 'Boh',
	   'dose': 100,
	   'interazione': None
	   }
	 }
	 #fingiamo che il piano è inserito
	 #il piano va salvato sempre o almeno una volta al giorno in json. qua va controlatto se ce n'è uno salvato o meno. Eventualmente con la modifica si sovrascrive
	if path.exists('piano.json')==True:

		with open('piano.json') as json_file:
    		piano = json.load(json_file)
	else:
#qua metto l'integrazione con la pagina
		piano=[{'orario':'20:30', 'medicina':'vivinC'}, {'orario':'10:00', 'medicina':'aspirina'},{'orario':'16:30', 'medicina':'tachipirina'}, {'orario':'16:30', 'medicina':'aspirina'}]
		piano=dati.riordina(piano)

		
	index, chiavi=dati.find_first(piano)
	d.print_med(chiavi[index], piano[chiavi[index]])
	ritardi={}
	for ora in piano.keys(): #creo un dizionari di ritardi a zero
		tmp={ora:0}
		ritardi.update(tmp)
	score=dati.algoritmo(piano, farmaci, ritardi)
	#devo inizializzzare i ritardi a zero e devo fare i primi punteggi con l'algoritmo che dovrebbe fare tutto insieme
	f, crit=dati.switch(score, chiavi[index])

	########main loop#########

	while 1:
		mid=dati.is_now('00:00')
		if mid==True:# se è mezzanotte aggiorno i punteggi
			score=dati.algoritmo(piano, farmaci, ritardi) #qua per i ritardi vanno messi come media. Ogni volta aggiungo dei nuovi ritardi e divido per 2
			f, crit=dati.switch(score, chiavi[index])
			with open('piano.json', 'w') as outfile:
    			json.dump(piano, outfile) #copia di backup una volta al giorno
			#male che va aggiorna pure il piano
		
		now=dati.is_now(chiavi[index])
		if now==True: #controllo se è l'ora
			msg=f'Ricordati di prendere {str(piano[chiavi[index]])[2:-2]}' #così dovrebbe fare schifo ma proviamo
			#manca la funzione che mi fermo dopo un'ora su message_loop
			rit=no.message_loop(msg, f, crit)
			ritardi.update({chiavi[index]:rit})
			index=index+1
			if index>(len(chiavi)-1):
				index=0
			d.print_med(chiavi[index], piano[chiavi[index]]) #stampo il prossimo "appuntamento"
			c.send_ts(rit) #mando i dati a thingspeak

		elif now==False:
			time.sleep(5) #dormi 5 secondi

