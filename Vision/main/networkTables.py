import numpy as np
import time
from networktables import NetworkTable
import logging


logging.basicConfig(level=logging.DEBUG)


ip = '10.4.1.2'


NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("SmartDashboard")


while True:
    x = np.random.rand() * 100
    y = np.random.rand() * 100
    sd.putNumber('x', x)
    sd.putNumber('y', y)     
    
    time.sleep(0.01)