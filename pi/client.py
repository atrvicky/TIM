"""
    Python MQTT Subscription client for raspberryPi
    This file has to be run on the raspberry that also
    hosts the mosquitto server.

    The processor section of this file is where different modules are 
    controlled based on user input

    The various components controlled are,
        1. Servos for the arms & the head - I2C on PCA9685 driver
        2. Ultrasound sensor
        3. OLED Screen

    The supported topics are
        1. larm
        2. rarm
        3. head
        4. oled
"""

import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit as sk
from time import sleep

# Don't forget to change the variables for the MQTT broker!
mqtt_username = "tim"
mqtt_password = "machine"
mqtt_topic = "chest"
mqtt_broker_ip = "192.168.0.111"
mqtt_broker_port = 1995

kit = sk(channels = 8)

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


# left upper arm = 0
ltUpArm = kit.servo[0]
# left lower arm = 1
ltLoArm = jit.servo[1]
# left shoulder = 2
ltSh = kit.servo[2]

# right upper arm = 3
rtUpArm = kit.servo[3]
# right lower arm = 4
rtLoArm = kit.servo[4]
# right shoulder = 5
rtSh = kit.servo[5]

# head = 6
hd = kit.servo[6]

def processor(topic, message):
    if (topic == "larmUp"):
        # control the left arm based on the coordinates obtained from the message
        if (message == "up"){
            kit.
        }
        return ""
    elif (topic == "larmRo"):
        return ""
    elif (topic == "larmLo"):
        return ""
    elif (topic == "rarmUp"):
        return ""
    elif (topic == "rarmRo"):
        return ""
    elif (topic == "rarmLo"):
        return ""
    elif (topic == "head"):
        # control the head based on the coordinate obtained from the message
        return ""
    elif (topic == "oled"):
        # control the oled based on the input obtained from the message
        return ""

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
