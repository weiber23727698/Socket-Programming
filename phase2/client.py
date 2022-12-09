import socket
import cv2
import pickle
import struct
import imutils
import time
import argparse
import numpy as np
import wave
import pyaudio

PORT = 8757
host_ip = '140.112.30.32'

def audio_stream(client_socket):
    p = pyaudio.PyAudio()
    BSIZE = 1024
    stream = p.open(
        format=p.get_format_from_width(2),
		channels=2,
		rate=44100,
		output=True,
		frames_per_buffer=BSIZE
    )
					
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            client_socket.settimeout(1)

            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame) 
        except socket.timeout:
            break

def video_stream(client_socket):
    data = b""
    payload_size = struct.calcsize("Q")
    
    while True:
        try:
            client_socket.settimeout(1)

            while (len(data)) < payload_size:
                packet = client_socket.recv(4*1024)
                if packet: 
                    data += packet
                else:
                    break
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            cv2.imshow("Vehicles", frame)
            key = cv2.waitKey(10)
            if key == 13:
                break
        except socket.timeout:
            break

def message_board(client_socket):
    print(client_socket.recv(1024).decode()) # previous record
    while True:
        message = input()
        client_socket.send(message.encode())
        if(message == "Finish"):
            break

def main():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host_ip, PORT))

    while True:
        print("What kind of features do you like?[audio/video/board] ", end="")
        feature = input()
        client_socket.send(feature.encode())
        if(feature == "video"):
            video_stream(client_socket)
        elif(feature == "audio"):
            audio_stream(client_socket)
        elif(feature == "board"):
            message_board(client_socket)
        else:
            print("no such feature !!!!!!")
        print("---------------------------------------------------")
        print("Would you like to continue?[yes/no] ", end="")
        choose = input()
        client_socket.send(choose.encode())
        if(choose == "no"):
            print("Thanks for your coming~")
            break
    
    client_socket.close()

if __name__ == "__main__":
    main()