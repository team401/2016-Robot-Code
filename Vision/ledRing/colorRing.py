import cv2
import numpy as np
import urllib.request
import time
from neopixel import *
 
# LED strip configuration:
LED_COUNT   = 16      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

count = 0

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
# Intialize the library (must be called once before other functions).
strip.begin()


# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://10.4.1.19/mjpg/video.mjpg')
bytes=b''

def colorCycle(count):
    while(count < 7):
        color =
        for i in LED_COUNT:
            setPixelColor(self, i, color)
    
    
    count = (count + 1)
    
    
while True:
    # Takes frames from the camera that we can use
    bytes+=stream.read(16384)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        img = frame[0:400, 0:640]

       # Displays the final product
        cv2.imshow('frame',frame)
        cv2.imshow('img',img)

     # Hit esc to kill
        if cv2.waitKey(1) ==27:
            exit(0)
            