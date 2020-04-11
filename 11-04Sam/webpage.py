import cherrypy
from MyMQTT import *
import json
import socket

class ProgettoIoT(object):
    exposed = True
    def __init__(self):
        self.mqtt=MyMQTT('pagina','localhost')
        self.mqtt.start()
    
    def POST(self, *uri, **params):
        # prendo i dati che mi interessano da params
        schedule = params
        # controllo che il file arrivi
       
        piano=self.ModificaSchedule(schedule)
        self.mqtt.myPublish('nomeutente/piano',json.dumps({'piano':piano}))



    # devo cambiare tutta la struttura del form e non ho ancora capito esattamente cosa uscirà lo faccio dopo
    def ModificaSchedule(self, schedule):
        print(f"\n\nIl form ricevuto è:\n{schedule}\n\n")
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
        print(dizionario)
        return dizionario

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


if __name__ == "__main__":
    conf = {
            '/':{
                    'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                    'tool.session.on':True
        }
    }
        
    cherrypy.tree.mount(ProgettoIoT(), '/', conf)
    IP=get_ip()
    cherrypy.config.update({'server.socket_host': IP}) #ip locale
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()