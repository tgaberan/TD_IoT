# python 3.6

import random
import json
import time
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

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.username_pw_set("englab","englab")
mqttc.connect(broker)
mqttc.loop_forever()
#print(f"Received the following message: {mqttc.user_data_get()}")

GPIO.cleanup()
print("exit")