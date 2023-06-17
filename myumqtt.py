import umqtt.robust
import mysecrets


class mqtt:
    def __init__(self):
        self._mq = umqtt.robust.MQTTClient(
            mysecrets.MQTTCLIENT,
            mysecrets.MQTTHOST,
            0, mysecrets.MQTTUSER,
            mysecrets.MQTTPASS,
            15)
        self._dv = f'{{"device":"{mysecrets.MQTTCLIENT}"'
        self._mq.set_callback(self._cb)

    def connect(self):
        self._mq.connect(True)

    def tick(self):
        # check need for ping
        self._mq.check_msg()

    def _cb(self, topic, msg):
        print(topic, msg)

    def _log(self, msg, level):
        m = f',"level":"{level}","msg":"{msg}"}}'
        m = self._dv + m
        print(m)
        self._mq.publish(mysecrets.MQTTBASE + "log", m, False, 1)

    def log_info(self, msg):
        self._log(msg, "info")

    def log_error(self, msg):
        self._log(msg, "error")

    def log_exception(self, msg):
        self._log(msg, "except")
        

if __name__ == "__main__":
    from time import sleep
    mq = mqtt()
    mq.connect()
    while 1:
        mq.tick()
        print("oh no!")
        mq.log_error("Oh no!")
        sleep(5)