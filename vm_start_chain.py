# Publish to ping
# Subscribe to pong

"""
Kaelyn Cho
Coding buddy: Jeremy Pogue

github repo: https://github.com/noonunnie/lab-04

"""

import paho.mqtt.client as mqtt
import time
import socket

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("kscho/pong")
    client.message_callback_add("kscho/pong", on_message_from_pong)

#Custom message callback for IP info.
def on_message_from_pong(client, userdata, message):
   time.sleep(1)
   print("Custom callback  - Pong: "+message.payload.decode())
   client.publish("kscho/ping", f"{int(message.payload.decode()) + 1}")

if __name__ == '__main__':

    # for local host
    # #get IP address
    # ip_address=socket.gethostbyname("localhost")

    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback functionto the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    # ee server
    # # Connect to the broker
    # client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)

    client.on_message = on_message_from_pong
    client.connect(host="192.169.0.109", port=1883, keepalive=60)

    # start the ping-pong chain by publishing the first number to ping
    userNumber = input("Choose starting number: ")
    client.publish("kscho/ping", f"{userNumber}")
    print("Welcome to ping-pong...")
    time.sleep(1)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_forever()
