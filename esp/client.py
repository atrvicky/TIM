"""
    Python MQTT Subscription client for esp module    

    The processor section of this file is where different modules are 
    controlled based on user input

    The various components controlled are,
        1. DC H-Bridge

    The supported topics are
        1. dcmt
"""

import paho.mqtt.client as mqtt

# Don't forget to change the variables for the MQTT broker!
mqtt_username = "tim"
mqtt_password = "machine"
mqtt_topic = "dcmt"
mqtt_broker_ip = "192.168.0.111"
mqtt_broker_port = 1995

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected: %s" % str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    print ("Topic: %s\nMessage: %s " % (str(msg.topic), str(msg.payload)))
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

    processor (msg.topic, msg.payload)

def processor(topic, message):
    if (topic == "dcmt"):
        # control the wheels based on the coordinates obtained from the message
        if (message == "lt"):
            # left
            motrCtrl(1,0)
            motrCtrl(2,1)

        elif (message == "rt"):
            # right
            motrCtrl(1,1)
            motrCtrl(2,0)

        elif (message == "fw"):
            # forward
            motrCtrl(1,1)
            motrCtrl(2,1)

        elif (message == "bw"):
            # backward
            motrCtrl(1,-1)
            motrCtrl(2,-1)

        elif (message == "st"):
            # stop
            motrCtrl(1,0)
            motrCtrl(2,0)

        elif (message == "sl"):
            # sharp left
            motrCtrl(1,-1)
            motrCtrl(2,1)

        elif (message == "sr"):
            # sharp right
            motrCtrl(1,1)
            motrCtrl(2,-1)
        

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, mqtt_broker_port)

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()
