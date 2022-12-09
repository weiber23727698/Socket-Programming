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

def audio_stream(client_socket):
    BSIZE = 1024
    audio = wave.open("song.wav", 'rb')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(
        format=p.get_format_from_width(audio.getsampwidth()),
        channels=audio.getnchannels(),
        rate=audio.getframerate(),
        input=True,
        frames_per_buffer=BSIZE
    )

    data = None
    if client_socket:
        count = 0
        while count < 1000:
            count += 1
            data = audio.readframes(BSIZE)
            a = pickle.dumps(data)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)


def video_stream(client_socket):
    if client_socket:
        vid = cv2.VideoCapture("b09902123.mp4")
        count = 0
        while (vid.isOpened() and count<135):
            count += 1
            time.sleep(0.1)
            success, frame = vid.read()
            frame = frame[::10, ::10, :] # lower the quality
            if success:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                key = cv2.waitKey(10)
                if key == 13:
                    client_socket.close()

def message_board(client_socket):
    f = open("text_board.txt", "r")
    prev = f.read()
    print(prev)

    client_socket.send(prev.encode())
    f = open("text_board.txt", "w")
    f.write(prev)

    while True:
        meg = client_socket.recv(1024).decode()
        if(meg == "Finish"):
            break
        print(meg)
        f.write(meg)
        f.write("\n")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('Host IP: ', host_ip)
    
    socket_address = (host_ip, PORT)
    server_socket.bind(socket_address)
    print("Socket bind successfully")
    server_socket.listen(5)
    print("Socket now listening")
    while True:
        client_socket, addr = server_socket.accept()
        print("========== New Connection ==========")
        while True:
            feature = client_socket.recv(1024).decode()
            if(feature == "video"):
                video_stream(client_socket)
            elif(feature == "audio"):
                audio_stream(client_socket)
            elif(feature == "board"):
                message_board(client_socket)
            else:
                print("no such feature !!!!!!")
            
            choose = client_socket.recv(1024).decode()
            if(choose == "no"):
                break
        
        client_socket.close()
    

if __name__ == "__main__":
    main()