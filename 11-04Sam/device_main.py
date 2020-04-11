import time
from DeviceMQTT import *


if __name__ == '__main__':
	#setup
	clientID="Device"
	broker='localhost'
	topic1='nomeutente/prox'
	topic2='nomeutente/notific'
	
	mqtt=DeviceMQTT(clientID, broker)
	mqtt.start()
	mqtt.mySubscribe(topic1)
	
	mqtt.mySubscribe(topic2)
	
	while True:

		time.sleep(5)
