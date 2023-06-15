from dotenv import load_dotenv
import pymongo
import os
from datetime import datetime


_db = None


def get_db():
    global _db
    if _db is None:
        load_dotenv()
        client = pymongo.MongoClient(os.getenv('MONGOCON'))
        _db = client.get_database("mongoqtt")
    return _db


#def insert_log(device:str, level:str, msg:str):
def insert_log(data:dict):
    data["dt"] = datetime.now()
    db = get_db()
    db["log"].insert_one(data)


if __name__ == "__main__":
    insert_log("bladev", "info", "hello there")