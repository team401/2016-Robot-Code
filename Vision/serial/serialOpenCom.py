import serial

distance = 420
angle = 69
x_coord = 9
y_coord = 8
goal = True

ser = serial.Serial('/dev/ttyS1', 9600, timeout=0) # Opens the Serial port

ser.write = ('{"distance":"' + str(distance) + '","angle":"' + str(angle) + '","x":"' + str(x_coord) + '","y":"' + str(y_coord) + '","goal":"' + str(goal) + '"}')