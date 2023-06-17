import umqtt.robust
import mysecrets
from myumqtthandler import handlers
import json

class mqtt:
    def __init__(self):
        self._mq = umqtt.robust.MQTTClient(
            mysecrets.MQTTCLIENT,
            mysecrets.MQTTHOST,
            0, mysecrets.MQTTUSER,
            mysecrets.MQTTPASS,
            15)
        self._dv = f'{{"device":"{mysecrets.MQTTCLIENT}",'
        self._mq.set_callback(self._cb)
        self._mc = 0

    def connect(self):
        self._mq.connect(True)
        for k in handlers:
            self._mq.subscribe(mysecrets.MQTTBASE + k)

    def tick(self):
        # check need for ping
        self._mq.check_msg()

    def _cb(self, topic, msg):
        try:
            hl = topic.split(mysecrets.MQTTBASE)[1]
            if hl in handlers:
                self.log_info(f"R: {hl} -> {msg}")
                handlers[hl](self, json.loads(msg))
            else:
                self.log_error("No Handler: " + topic)
        except:
            self.log_exception(f"Ex: {topic} - {msg}")

    def _log(self, msg, level):
        m = msg.replace('"', '\\"')
        m = f'"c":{self._mc},"level":"{level}","msg":"{m}"}}'
        self._mc += 1
        m = self._dv + m
        self._mq.publish(mysecrets.MQTTBASE + "log", m, False, 1)

    def log_info(self, msg):
        self._log(msg, "info")

    def log_error(self, msg):
        self._log(msg, "error")

    def log_exception(self, msg):
        self._log(msg, "except")

    def pub(self, topic, message:dict, qos=0):
        message["device"] = mysecrets.MQTTCLIENT
        message["c"] = self._mc
        self._mc += 1
        self._mq.publish(mysecrets.MQTTBASE + topic, json.dumps(message), False, qos)
        

if __name__ == "__main__":
    from time import sleep
    mq = mqtt()
    mq.connect()
    while 1:
        mq.tick()
        #print("oh no!")
        #mq.log_error("Oh no!")
        sleep(0.2)