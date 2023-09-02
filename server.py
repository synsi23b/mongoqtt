#!/usr/bin/python3

from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os
from time import sleep
import traceback
import json
from pahohandler import handlers
import logging
from threading import Thread
from webio import launch as run_webio
import time


load_dotenv()


client_name = os.getenv("MQTT_USER") + "test"
client = mqtt.Client(client_name, clean_session=False)
client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))


base = os.getenv("BASE_TOPIC")


_logstacks = {}


def _clean_stack(name):
    stack = _logstacks.get(name, [])
    stamp = time.time()
    stack = [ x for x in stack if (stamp - x[1]) < 10 ]
    _logstacks[name] = stack
    return stack


def _test_no_duplicate(msgcount, stack):
    for c, s in stack:
        if msgcount == c:
            return False
    return True


def _no_hdnl(top, data):
    logging.error(f"No handler for {top} -> {data}")


def on_message(client, userdata, message):
    try:
        data = str(message.payload.decode("utf-8"))
        data = json.loads(data)
        top = message.topic.split(base)[1]
        stack = _clean_stack(data.get("device", "unknown"))
        msgcount = data.get("c", -1)
        if msgcount < 0:
            handlers.get(top, _no_hdnl)(top, data)
        elif _test_no_duplicate(msgcount, stack):
            stack.append((msgcount, time.time()))
            handlers.get(top, _no_hdnl)(top, data)
        else:
            print(f"ignore duplicate {top} {msgcount}")
        #print("message received ", data)
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)
    except json.JSONDecodeError:
        logging.error("Json decode Error")
        logging.error(f"Topic: {message.topic}")
        logging.error(f"Data: {data}")
    except Exception:
        logging.error("Exception on_message:")
        logging.error(f"Topic: {message.topic}")
        logging.error(f"Data: {data}")
        traceback.print_exc()
    

client.on_message = on_message

host = os.getenv("MQTT_HOST")
print(f"Attempting MQTT connect to {host}")
res = client.connect(host, keepalive=20)
print("Mqtt connect result: ", res)
#client.loop_start()


for k in handlers:
    topic = f"{base}/{k}"
    print(f"Subscribing to {topic}")
    client.subscribe(topic)


while True:
    try:
        Thread(target=run_webio, args=(client, base)).start()
        client.loop_forever()
    except:
        traceback.print_exc()
        break


#client.loop_stop()
print("MQTT client finished")