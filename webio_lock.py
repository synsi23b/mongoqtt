from pywebio.input import input
from pywebio.output import put_buttons, toast, put_table, use_scope, clear_scope


commands = [
    ("test1", ("foo", "bar")),
    ("test2", ("barfoo", "bar2"))
]

def btn_click(val):
    toast(val)


def app(v:str):
    put_buttons(commands, btn_click)