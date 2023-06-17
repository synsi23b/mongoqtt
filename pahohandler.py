from mongo import insert_log
import time
import queue

handlers = {}


def log(top:str, data:dict):
    insert_log(data)

handlers["log"] = log


import webio_lock
handlers["lock"] = webio_lock.put_message
