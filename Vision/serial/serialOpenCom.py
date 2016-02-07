import serial

ser = serial.Serial('/dev/ttyS1', 9600, timeout=0) # Opens the Serial port
liamAwesome = False
ser.write(b'what only strings?' + str(liamAwesome))