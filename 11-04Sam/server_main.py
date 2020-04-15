####server####


from dati import *
import time
import json
from ServerMQTT import *
from os import path

if __name__ == '__main__':
	#setup
	with open('farmaci.json') as json_file:
			farmaci = json.load(json_file)
	
   	with open("log_server.json", "r") as f:
        settings = json.load(f)

    	clientID = settings["clientID"]
   	broker = settings["broker"]
    	topic1 = settings["topic_ritardi"]
    	topic2 = settings["topic_prossimo_orario"]
	topic3 = settings["topic_piano"]
    	topic4 = settings["notifica"]
	dati=dati()
	mqtt=ServerMQTT(clientID, broker)
	mqtt.start()
	mqtt.mySubscribe(topic1)
	mqtt.mySubscribe(topic3)
	
	
	#controllo se esiste già un backup del piano. In caso di problemi al server appena ritorna online sa già cosa deve fare
	if path.exists('piano.json')==False:
		while mqtt.piano=={}:
			
			time.sleep(5)
	else:
		with open('piano.json') as json_file:
			mqtt.piano = json.load(json_file)

	#seleziono il prossimo appuntamento
	mqtt.index, mqtt.chiavi=dati.find_first(mqtt.piano)
	
	
	#comunico subito le informazioni al display
	mqtt.myPublish(topic2, json.dumps({'medicine': mqtt.piano[mqtt.chiavi[mqtt.index]], 'orario':mqtt.chiavi[mqtt.index]})) #da mandare per il display
	
	
	for ora in mqtt.piano.keys(): #creo un dizionari di ritardi a zero
		tmp={ora:0}
		mqtt.ritardi.update(tmp)
	
	#calcolo i punteggi
	score=dati.algoritmo(mqtt.piano, farmaci, mqtt.ritardi)
	
	#creo un backup locale per il piano
	piano_backup=mqtt.piano

	while True:
		#controllo se il backup

		if piano_backup!=mqtt.piano: #se il piano è cambiato
			#aggiorno il prossimo step e lo invio
			mqtt.index, mqtt.chiavi=dati.find_first(mqtt.piano)
			mqtt.myPublish(topic2, json.dumps({'medicine': mqtt.piano[mqtt.chiavi[mqtt.index]], 'orario':mqtt.chiavi[mqtt.index]})) #da mandare per il display
			#qua aggiorno i ritardi
			mqtt.ritardi=dati.ritardi_update(mqtt.piano, mqtt.ritardi)
			#aggiorno lo score
			score=dati.algoritmo(mqtt.piano, farmaci, mqtt.ritardi)
			



		#cose da fare a fine giornata
		mid=dati.is_now('00:00')
		if mid==True:# se è mezzanotte aggiorno i punteggi
			score=dati.algoritmo(piano, farmaci, mqtt.ritardi) #qua per i ritardi vanno messi come media. Ogni volta aggiungo dei nuovi ritardi e divido per 2
			#salvo il piano come json come backup
			with open('piano.json', 'w') as outfile:
				json.dump(mqtt.piano, outfile)

			#dormo per 1 minuto sennò rientra nell'if
			time.sleep(60)


		#codice del quando è ora
		now=dati.is_now(mqtt.chiavi[mqtt.index])
		if now==True: #controllo se è l'ora
			#calcolo i parametri da inviare
			f, crit=dati.switch(score, mqtt.chiavi[mqtt.index])
			msg=f'Ricordati di prendere {str(mqtt.piano[mqtt.chiavi[mqtt.index]])[2:-2]}' 

			#qui controllo che non sia l'ultimo orario della giornata per calcolare il ritardo massimo

			if mqtt.index>(len(mqtt.chiavi)-2):
				mqtt.ritm=dati.ritmax(mqtt.chiavi[mqtt.index], "24:00")
			else:
				mqtt.ritm=dati.ritmax(mqtt.chiavi[mqtt.index], mqtt.chiavi[mqtt.index+1])

			#mando i dati e dormo per 1 minuto
			mqtt.myPublish(topic4, json.dumps({'messaggio': msg, 'frequenza':f, 'n_msg_critici':crit, 'ritardo_massimo':mqtt.ritm}))
			time.sleep(60)

			
		elif now==False:
			time.sleep(5) #dormi 5 secondi





