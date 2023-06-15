from mongo import insert_log

handlers = {}

def log(data:dict):
    insert_log(data)

handlers["log"] = log
