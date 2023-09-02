from pywebio.session import register_thread
from pywebio.input import input
from pywebio.output import put_buttons, toast, put_table, put_text, use_scope, clear
from threading import Thread
import queue


mqtt_cl = None
mqtt_bs = ""
mqtt_in = queue.Queue()


commands = [
    ("test1", ("foo", '{"foo":"bar"}')),
    ("test2", ("barfoo", "[1,2,3]"))
]


def btn_click(val):
    put_text(f"Exec: {val[0]}")
    mqtt_cl.publish(f"{mqtt_bs}lockcom", val[1])


def put_message(top, msg):
    mqtt_in.put(msg)


def _run():
    while True:
        m = mqtt_in.get()
        put_text(m["msg"])


def app(mqtt_client, base_topic):
    global mqtt_cl
    global mqtt_bs
    mqtt_cl = mqtt_client
    mqtt_bs = base_topic
    mqtt_client.subscribe(f"{base_topic}lock")
    put_buttons(commands, btn_click)
    t = Thread(target=_run)
    register_thread(t)
    t.start()

