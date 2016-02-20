import threading
print(threading.__file__)

TOTAL = 0
number = 0

#class CountThread(threading.Thread):
#    def run(self):
#        global TOTAL
#        for i in range(100):
#            TOTAL = TOTAL + 1
#        print('%s\n' % (TOTAL))
        

def printing():
    global number
    print(number)
    number = number + 1

#a = CountThread()
#b = CountThread()

a = threading.Thread(target=printing)
b = threading.Thread(target=printing)

a.start()
b.start()

#while(1):
#    a.run()
#    b.run()
#    sleep(0.5)

    