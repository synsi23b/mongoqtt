from dotenv import load_dotenv
import pymongo
import os
from datetime import datetime


load_dotenv()
_db = client.get_database("mongoqtt")


#def insert_log(device:str, level:str, msg:str):
def insert_log(data:dict):
    data["dt"] = datetime.now()
    _db["log"].insert_one(data)


if __name__ == "__main__":
    insert_log("bladev", "info", "hello there")