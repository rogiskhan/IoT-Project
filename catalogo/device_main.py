  
import time
import json
# from DeviceMQTT import *
from send_catalog import *
import requests
from config import *
if __name__ == '__main__':
    # setup
    c=Config()
    c.getserial()
    c.log()
    # mqtt=DeviceMQTT()
    # mqtt.start()
    # mqtt.mySubscribe(mqtt.topic1)

    # mqtt.mySubscribe(mqtt.topic2)

    # t = threading.Thread(target=mqtt.waiting_msg)
    # t.start()
    t = perpetualTimer(5, send_get,[{'ID': "silvia",'serial_number':"disp1"}])
    t.start()
    
    
   
    
    # while True:
    #     r=requests.get('http://127.0.0.1:8080') 
    #     time.sleep(10)

    
   