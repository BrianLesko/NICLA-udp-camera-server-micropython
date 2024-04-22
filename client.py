
# display the image in the client using streamlit web browser

import socket
import cv2
import numpy as np
import streamlit as st
import customize_gui as gui
gui = gui.gui()

gui.setup(wide=True,text="Receive a video stream from a Nicla Vision UDP camera server.")
st.title("UDP Camera Client")
image_spot = st.empty()

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the client to a specific address (optional)
client_address = ('172.20.10.2', 8000)  # Replace with the client's IP address and port
client.bind(client_address)
print('Client is listening at', client_address)

def display():
    data = b''  # initialize the data variable
    while True:
        with st.spinner('Waiting for the next chunk...'):
            chunk, addr = client.recvfrom(900000000)
        if chunk == b'CAM':
            data = b''
        elif chunk == b'END':  # check for the "END" delimiter
            chunk, addr = client.recvfrom(900000000)
            try: 
                # print the length of the data
                frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                # show the image
                with image_spot:
                    st.image(frame, channels="BGR", width=800)  # Set the width to the desired value
            except:
                print('Error deserializing the frame')
            data = b''  # reset the data for the next frame
            print('Frame received')
            break
        else:
            data += chunk

while True:
    with st.spinner('Waiting for the next chunk...'):
        chunk, addr = client.recvfrom(900000000)
    if chunk == b'CAM':
        display()
    else:
        print("Not a camera stream transmission")


