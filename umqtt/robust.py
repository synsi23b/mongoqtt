import paho.mqtt.client as mqtt
import queue

class MQTTException(Exception):
    pass


class MQTTClient:
    def __init__(
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=False,
        ssl_params={},
    ):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False
        self.paho = None
        self.paho_queue = queue.Queue()
        self.paho_block = True

    def _paho_cb_wrapper(self, client, userdata, message):
        self.paho_queue.put((message.topic, message.payload.decode("utf-8")))

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        self.paho = mqtt.Client(self.client_id, clean_session=clean_session)
        self.paho.username_pw_set(self.user, self.pswd)
        self.paho.on_message = self._paho_cb_wrapper
        self.paho.connect(self.server, self.port, self.keepalive)
        self.paho.loop_start()

    def disconnect(self):
        self.paho.disconnect()

    def ping(self):
        pass

    def publish(self, topic, msg, retain=False, qos=0):
        self.paho.publish(topic, msg, qos, retain)

    def subscribe(self, topic, qos=0):
        self.paho.subscribe(topic, qos)

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        if self.paho_block:
            self.cb(*self.paho_queue.get())
            return 2
        else:
            self.paho_block = True
            try:
                msg = self.paho_queue.get_nowait()
            except queue.Empty:
                return None
            self.cb(*msg)
            return 2

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        self.paho_block = False
        return self.wait_msg()