import serial
import numpy as np
import io

ser = serial.Serial('/dev/ttyS0', 115200, timeout=0) # Opens the Serial port
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


while(True):
    sio.flush()


    hello = sio.readline()

    if(hello == 's'):
	distance = np.random.rand()
	angle = np.random.rand()
	x_coord = np.random.rand()
	y_coord = np.random.rand()
	goal = True
	packet = '{"distance":"' + str(round(distance, 3)) + '","angle":"' + str(round(angle,3)) + '","x":"' + str(round(x_coord,3)) + '","y":"' + str(round(y_coord,3)) + '","goal":"' + str(goal) + '"}'  + '\n'
	try:
		ser.write(packet.encode())
	except Exception as e:
		print e
	print(packet)
