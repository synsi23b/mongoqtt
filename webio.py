import pywebio
from pywebio.input import input
from pywebio.output import put_buttons, toast, put_table, put_scope, put_text, use_scope, clear, remove
import webio_lock
from dotenv import load_dotenv
import os


load_dotenv()


mqtt = None
base_top = ""

def noop(v:str):
    print(v)


apps = [
    ("Main door functions", ("Main door functions", webio_lock.app)),
    ("test2", ("noop", noop))
]


def login():
    def check(pw):
        if pw != os.getenv("WEBIO_PASS"):
            return "Wrong password!"
    input("Input your password:", validate=check)


def return_to_main(v):
    show_menu()


def btn_click(app):
    clear()
    put_buttons(["Return to main menu"], return_to_main)
    dsc, app = app
    put_text(dsc)
    app(mqtt, base_top)


def show_menu():
    clear()
    put_buttons(apps, onclick=btn_click)


def main():
    try:
        login()
        show_menu()
    except Exception as e:
        toast(f"Error: {e}")


def launch(mqtt_client, base_topic):
    global mqtt
    global base_top
    mqtt = mqtt_client
    base_top = base_topic
    pywebio.start_server(main, port=os.getenv("WEBIO_PORT"))


if __name__ == '__main__':
    pywebio.start_server(main, port=os.getenv("WEBIO_PORT"))