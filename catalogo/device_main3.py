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

	t1 = perpetualTimer(5, send_get,[{'ID': "igor",'serial_number':"disp1"}])
	t1.start()