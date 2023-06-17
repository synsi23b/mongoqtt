#!/usr/bin/python3

from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os
from time import sleep
import traceback
import json
from pahohandler import handlers


load_dotenv()


client_name = os.getenv("MQTT_USER")
client = mqtt.Client(client_name, clean_session=False)
client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))


base = os.getenv("BASE_TOPIC") + "/"


def on_message(client, userdata, message):
    try:
        data = message.payload.decode("utf-8")
        print("message received ", data)
        print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)
        hdl = handlers.get(message.topic.split(base)[1], None)
        if hdl:
            hdl(json.loads(str(data)))
    except Exception:
        traceback.print_exc()
    

client.on_message = on_message

host = os.getenv("MQTT_HOST")
print(f"Attempting MQTT connect to {host}")
res = client.connect(host, keepalive=20)
print("Mqtt connect result: ", res)
client.loop_start()


for k in handlers:
    topic = f"{base}{k}"
    print(f"Subscribing to {topic}")
    client.subscribe(topic)


while True:
    try:
        client.loop_forever()
    except:
        traceback.print_exc()
        break


client.loop_stop()
print("MQTT client finished")