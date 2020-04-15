import time
import json
from DeviceMQTT import *
from catalog import *
from send_catalog import *

if __name__ == '__main__':
    # setup
    with open("device_log.JSON", "r") as f:
        settings = json.load(f)

    clientID = settings["clientID"]
    broker = settings["broker"]
    topic1 = settings["topic_ritardi"]
    topic2 = settings["topic_prossimo_orario"]


    mqtt=DeviceMQTT(clientID, broker)
    mqtt.start()
    mqtt.mySubscribe(topic1)

    mqtt.mySubscribe(topic2)

    # creo il catalogo
    catalogClient = CatalogREST('Catalog')


    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80})
    cherrypy.tree.mount(catalogClient, '/', conf)
    cherrypy.engine.start()

    # invio le ID di tutti i dispositivi e servizi connessi
    # (per ora faccio l'esempio con il solo dispositivo Display e il servizio Algoritmo)
    t = perpetualTimer(5, send,[{'ID': "Display"}, {'ID': "Algoritmo"}])
    t.start()


    while True:
        catalogClient.catalog.removeInactive()
        with open("catalogo.json", "w") as f:
            json.dump(catalogClient.catalog.devices, f)
        time.sleep(5)
    cherrypy.engine.exit()