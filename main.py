import time
import sys
import grovepi

ultrasonic_ranger = 3

while True:
    print("Working")
    try:
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)
        # change range here
        if distance < 30:
            print("Detected: Wait like 20sec")
            exec(open("facial_recognition.py").read())
            time.sleep(300)
        else:
            time.sleep(1)
    except KeyboardInterrupt:
        break
    except IOError:
        print("Error")
