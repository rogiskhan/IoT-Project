import os
import pathlib


def add_user(ID):
	path=pathlib.Path().absolute() #salvo il path
	os.mkdir(ID) #creo la cartella vuota
	os.cd(path + "Template/user") #vado nella cartella dei templates
	command="cp -R * " + path + "/" + ID #comando in bash per copiare tutto (importo mwno librerie)
	os.system(command) #eseguo il comando
	os.cd(path + "/" + ID) #vado nella cartella dell'utente
	with open("log_server.json", "r") as f:
		settings = json.load(f)
	settings.update({"ID": ID})
	command="sudo python3 server_main.py"
	os.system(command)
