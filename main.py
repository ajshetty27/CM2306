import time
import sys
import grovepi

#Detect ultrasonic sensor on port 3
ultrasonic_ranger = 3

while True:
    print("Working")
    try:
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)
        #Range of detection of ultrasonic sensor 
        if distance < 30:
            print("Detected: Wait like 20sec")
            #If face is detected run facial recognition
            exec(open("facial_recognition.py").read())
            time.sleep(300)
        else:
            time.sleep(1)
    except KeyboardInterrupt:
        break
    except IOError:
        print("Error")
