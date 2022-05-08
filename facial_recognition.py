import face_recognition
import cv2
import numpy as np
import os
import glob
import grovepi
import sys
import time
import datetime

#Implement code required for LCD BackLight 

if sys.platform == 'uwp':
    import winrt_smbus as smbus

    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO

    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e


# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r, g, b):
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)


# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)


# set display text \n for second line(or auto wrap)     
def setText(text):
    textCommand(0x01)  # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04)  # display on, no cursor
    textCommand(0x28)  # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))


# Get a reference to raspberry pi camera 
video_capture = cv2.VideoCapture(0)

# make array of sample pictures with encodings
known_face_encodings = []
known_face_names = []
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'known_people/')

# make an array of all the saved jpg files' paths
list_of_files = [f for f in glob.glob(path + '*.jpg')]
# find number of known faces
number_files = len(list_of_files)

names = list_of_files.copy()

for i in range(number_files):
    # load image
    image = face_recognition.load_image_file(list_of_files[i])
    # find face encodings
    face_encoding = face_recognition.face_encodings(image)[0]
    # add face encoding to array
    known_face_encodings.append(face_encoding)

    # Create array of known names
    names[i] = names[i].replace("known_people/", "")
    known_face_names.append(names[i])

# Initialize variables hold values 
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
spammer = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    intruder_path = os.path.join(dirname, 'intruder_images/')
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        if name != "Unknown":
            cv2.putText(frame, name[:-4], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #Display name on LCD 
            setText("Welcome " + name[:-4])
            setRGB(0, 128, 64)
        else:
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #Display Inrtuder message on LCD
            setText("Intruder Alert")
            setRGB(0, 128, 64)
            #Create image of intruder and save to intruder folder 
            cv2.imwrite(intruder_path + str(datetime.datetime.now()) + ".jpg", frame)
            if spammer < 1:
                exec(open("send_email.py").read())
                exec(open("send_sms.py").read())
                spammer += 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to display on Raspberry pi
video_capture.release()
cv2.destroyAllWindows()
