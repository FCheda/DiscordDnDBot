import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint

load_dotenv()
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_server = os.getenv("MONGO_SERVER")


class mongo_connector:
    client = None

    def __init__(self):
        self.client = mongo_connector.get_connection()

    def get_connection():
        connection_str = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_server}/?retryWrites=true&w=majority"
        client = MongoClient(connection_str)
        return client


if __name__ == "__main__":
    print("testing mongo connection")
    connector = mongo_connector()
    db = connector.client["d&d_server_main_db"]
    print(db)
    collection = db["test"]
    print(collection)
    pprint.pprint(collection.find_one())
