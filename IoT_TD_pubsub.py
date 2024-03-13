# python 3.6

import random
import json
import time
import math
import Adafruit_BBIO.GPIO as GPIO

from paho.mqtt import client as mqtt_client


broker = '213.32.88.153'
port = 1883
topic = "/1/ctrl"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = 'englab'
password = 'englab'


import paho.mqtt.client as mqtt

def setOuptut():
    GPIO.output("P8_10", GPIO.HIGH)


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        print(userdata)
        #userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    wMsgPayload = message.payload
    print(wMsgPayload)
    m_in = json.loads(wMsgPayload)
    if( m_in["led"] == 1 ):
        print("led ON")
        GPIO.output("P8_10", GPIO.HIGH)
    else:
        print("led OFF")
        GPIO.output("P8_10", GPIO.LOW)
    # We only want to process 10 messages
    #client.unsubscribe("#")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(topic)


GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_14", GPIO.IN)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.on_publish = on_publish

mqttc.username_pw_set("englab","englab")
mqttc.connect(broker)

mqttc.loop_start()
#print(f"Received the following message: {mqttc.user_data_get()}")


for i in range(1,500):
    
    wMsg = ""
    if GPIO.input("P8_14"):
        wMsg = "\"switch\":true"
    else:
        wMsg = "\"switch\":false"
    wSin = 50.0 + math.sin(i*5*math.pi/180)*50.0
    wSin = round(wSin, 1)
    wMsg += ",\"temp\":"+str(wSin)
    wMsg = "{"+wMsg+"}"
    
    print(wMsg)
    msg_info = mqttc.publish("/1/sensor", wMsg, qos=1)
    msg_info.wait_for_publish()
    time.sleep(0.5)


GPIO.cleanup()
print("exit")