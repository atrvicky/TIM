"""
    Python MQTT Subscription client for esp module    

    The processor section of this file is where different modules are 
    controlled based on user input

    The various components controlled are,
        1. DC H-Bridge

    The supported topics are
        1. dcmt
"""

from umqtt.robust import MQTTClient as mqtt
from machine import Pin as pin


# Don't forget to change the variables for the MQTT broker!
mqtt_username = "tim"
mqtt_password = "machine"
mqtt_topic = "dcmt"
mqtt_broker_ip = "192.168.0.111"
mqtt_broker_port = 1995

client_id = 'esp_tim'

client = mqtt(client_id, mqtt_broker_ip, mqtt_broker_port, mqtt_username, mqtt_password)
client.DEBUG = True


# mode - 0 => st
# mode - 1 => fw
# mode - 2 => bw

#motPin - 1 => left motor
#motPin - 2 => right motor
def motrCtrl(motPin, mode):
        p1 = pin(4, pin.OUT)
        p2 = pin(5, pin.OUT)

        p3 = pin(0, pin.OUT)
        p4 = pin(2, pin.OUT)

        e1 = pin(14, pin.OUT)
        e2 = pin(12, pin.OUT)
        
        #p1 = pin(12, pin.OUT)
        #p2 = pin(14, pin.OUT)

        #p3 = pin(13, pin.OUT)
        #p4 = pin(15, pin.OUT)
        
        e1.value(1)
        e2.value(1)
        if (motPin == 1):
                if (mode == 0):
                        p1.value(0)
                        p2.value(0)
                elif (mode > 0):
                        p1.value(1)
                        p2.value(0)
                elif (mode < 0):
                        p1.value(0)
                        p2.value(1)
        elif (motPin == 2):
                if (mode == 0):
                        p3.value(0)
                        p4.value(0)
                elif (mode > 0):
                        p3.value(1)
                        p4.value(0)
                elif (mode < 0):
                        p3.value(0)
                        p4.value(1)

motrCtrl(1, 0)
motrCtrl(2, 0)

def on_message(topic, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    
    print ("Topic: %s\nMessage: %s " % (str(topic), str(msg)))
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

    processor (topic, msg)

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
        
def start():
    connected = client.connect()
    if (connected == 0):
        print ('connected to broker')

        client.set_callback(on_message)
        client.subscribe(b'dcmt')

        while True:
            client.wait_msg()
    else:
        print('error!')