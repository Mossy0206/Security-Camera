import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import time

HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr=s.accept()
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
face_cascade2 = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(10000)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.24, minNeighbors=4)
    faces2 = face_cascade2.detectMultiScale(gray, scaleFactor=1.24, minNeighbors=4)
    stroke = 2
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        img_item = "my_image.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255, 0, 0)
        stroke = 2
        width = x + w
        height = y + h
        cv2.rectangle(frame, (x, y), (width, height), color, stroke)
    for (x, y, w, h) in faces2:
        roi_gray = gray[y:y + h, x:x + w]
        img_item = "my_image2.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255, 0, 0)
        stroke = 2
        width = x + w
        height = y + h
        cv2.rectangle(frame, (x, y), (width, height), color, stroke)
    cv2.imshow('CCTV', frame)
    out.write(frame)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break


out.release()
cv2.destroyAllWindows()