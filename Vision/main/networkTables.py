import sys
import time
from networktables import NetworkTable
import logging


logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

ip = sys.argv[1]

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("SmartDashboard")


while True:
    try:
        print('robotTime:', sd.getNumber('robotTime'))
    except KeyError:
        print('robotTime: N/A')

    sd.putNumber('distance', distance)
    sd.putNumber('angle', angle)
    sd.putNumber('x', x)
    sd.putNumber('y', y)     
    
    time.sleep(1)