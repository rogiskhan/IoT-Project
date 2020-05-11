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

    t2 = perpetualTimer(5, send_get1,[{'ID': "elena",'serial_number':"disp3"}])
    t2.start()