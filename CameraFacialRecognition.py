import cv2
import numpy as np
import time
import socket
import pickle
import zlib
import struct
import io
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.137', 8485))
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
connection = client_socket.makefile('wb')
cap = cv2.VideoCapture(0)
img_counter = 0
while True:
    check, frame = cap.read()
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1


cap.release()
cv2.destroyAllWindows()
