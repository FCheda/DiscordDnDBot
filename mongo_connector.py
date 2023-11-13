import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint
import random

load_dotenv()
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_server = os.getenv("MONGO_SERVER")

dbname = "d&d_server_main_db"
character_collection = "test"
player_collection = "test_player"


class mongo_connector:
    client = None

    def __init__(self):
        self.client = mongo_connector.get_connection()

    def get_connection():
        connection_str = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_server}/?retryWrites=true&w=majority"
        client = MongoClient(connection_str)
        return client

    def get_character(self, character_name: str = None):
        print("character is ", character_name)
        if character_name is not None:
            return self.client[dbname][character_collection].find_one(
                {"Personaje": character_name}
            )
        else:
            return self.client[dbname][character_collection].find_one()

    def get_player(self, player_name: str = None):
        print("player is ", player_name)
        if player_name is not None:
            return self.client[dbname][player_collection].find_one(
                {"Nombre": player_name}
            )
        else:
            return self.client[dbname][player_collection].find_one()

    def update_character(self, character_name=None, dict=None):
        if character_name is not None:
            if dict is not None:
                newvalues = {"$set": dict}
                self.client[dbname][character_collection].update_one(
                    {"Personaje": character_name}, newvalues
                )
            else:
                newvalues = {"$set": {"rabo": f"{random.randint(0,20)} cm"}}
                self.client[dbname][character_collection].update_one(
                    {"Personaje": character_name}, newvalues
                )


if __name__ == "__main__":
    print("testing mongo connection")
    connector = mongo_connector()
    db = connector.client["d&d_server_main_db"]
    print(db)
    collection = db["test"]
    print(collection)
    pprint.pprint(connector.get_character("Glaurimm"))
