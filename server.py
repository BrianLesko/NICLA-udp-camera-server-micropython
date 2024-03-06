# Brian Joseph Lesko        2/1/24      Robotics Automation Engineer III
# Create a LAN server that hosts a live data feed generated from the host machine 

import numpy as np
import cv2 # pip install opencv-python-headless
import socket
import pickle

camera = cv2.VideoCapture(0) # on a mac you can use either your mac webcam or an iphone camera using continuity camera! for me, my iphone was (1) and my mac webcam was (0) 
# Limit the size and FPS to increase speed
camera.set(cv2.CAP_PROP_FPS, 24) # FPS
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # compression method

def get_frame(): 
    global camera
    try: 
        _, frame = camera.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # this line flips the image
        return frame
    except:
        return np.zeros((300, 300, 3))

def main():
    #st.set_page_config(layout="wide")
    #st.title("Live Camera Feed")

    # UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('Host:', host_ip)
    server.bind((host_ip, 8000))  # Bind the socket to a specific address

    client_address = ('127.0.0.1', 8001)  # Replace with the client's IP address and port

    while True:
        frame = get_frame()
        #data = pickle.dumps(frame)
        data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Split the data into chunks
        chunk_size = 500  # Maximum UDP packet size
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            server.sendto(chunk, client_address)
        #print("frame sent", len(data))
        server.sendto(b'END', client_address)  # send an empty chunk to signal the end of the frame
        
main() 