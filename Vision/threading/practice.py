import threading

number=0
lock=threading.Lock()

def printing1(increment):
    global number
    while (number < 500):
        lock.acquire()
        try:
            print("ONE: " + str(number))
            number = number + increment
        finally:
            lock.release()
            
def printing2(increment):
    global number
    while (number < 500):
        lock.acquire()
        try:
            print("TWO: " + str(number))
            number = number + increment
        finally:
            lock.release()
            
            
a = threading.Thread(target=printing1, args=[10])
b = threading.Thread(target=printing2, args=[5])

a.start()
b.start()


a.join()
b.join()