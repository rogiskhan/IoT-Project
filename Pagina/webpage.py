import cherrypy
import os
from jinja2 import Template #Environment, FileSystemLoader
import json
import socket
from MyMQTT import *



class ProgettoIoT(object):
	exposed = True
	def __init__(self):
		with open("log_pagina.json", "r") as f:
			setting = json.load(f)
			clientID=setting["clientID"]
			broker=setting["broker"]
			self.topic="ID/piano"
		self.mqtt=MyMQTT(clientID, broker)
		self.mqtt.start()
		
	def GET(self):
		file = open('Pagina.html')
		content = file.read()
		file.close()
		template = Template(content)
		ipasda = get_ip()
		self.output = template.render(ip=ipasda)
		return self.output


	def POST(self, *uri, **params):
		new_s = ModificaSchedule(params)
		self.mqtt.myPublish(self.topic, json.dumps({'piano': new_s}))
		print(new_s)
		file = open('Pagina.html')
		content = file.read()
		file.close()
		template = Template(content)
		ipasda = get_ip()
		self.output = template.render(ip=ipasda, Schedule = json.dumps(params))
		return self.output

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP


def ModificaSchedule(schedule):
	dizionario = {}
	liste = []
	keys = []
	for names in schedule.keys():
		if "Orario_" in names:
			keys.append(schedule[names])
			lista = []
			indice = names.replace("Orario_", "")
			nuova_str = "Medicinale_" + indice + "_"
			for names in schedule.keys():
				if nuova_str in names:
					lista.append(schedule[names])
			liste.append(lista)
	# in keys ho una lista degli orari(che saranno le keys del dizionario)
	# in liste ho le liste di medicinali corrispondenti a ciascun orario
	n_orari = len(keys)
	for i in range(n_orari):
		dizionario[keys[i]]= liste[i]
	return dizionario


if __name__ == "__main__":
	conf = {
			'/':{
					'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
					'tools.staticdir.root': os.path.abspath(os.getcwd()),
					'tool.session.on':True
				},
			'/js':{
					'tools.staticdir.on': True,
					'tools.staticdir.dir':'./js'
				},
			'/css':{
					'tools.staticdir.on': True,
					'tools.staticdir.dir':'./css'
				},
	}
		
	cherrypy.tree.mount(ProgettoIoT(), '/', conf)
	IP=get_ip()
	cherrypy.config.update({'server.socket_host': IP}) #ip locale
	cherrypy.config.update({'server.socket_port': 80})
	cherrypy.engine.start()
	cherrypy.engine.block()
