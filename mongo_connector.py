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
logs_collection = "test_log"
class_collection = "test_classes"
race_collection = "test_races"


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

    def update_player(self, player_name=None, dict=None):
        if player_name is not None:
            if dict is not None:
                newvalues = {"$set": dict}
                self.client[dbname][player_collection].update_one(
                    {"Personaje": player_name}, newvalues
                )
            else:
                newvalues = {"$set": {"rabo": f"{random.randint(0,20)} cm"}}
                self.client[dbname][player_collection].update_one(
                    {"Personaje": player_name}, newvalues
                )

    def insert_log(self, dict=None):
        if dict is not None:
            self.client[dbname][logs_collection].insert(dict)
        else:
            return None

    def insert_character(self, dict=None):
        if dict is not None:
            return self.client[dbname][character_collection].insert(dict)
        else:
            return None

    def get_classes(self, filter: dict = None, format: str = None):
        cursor = self.client[dbname][class_collection].find(filter)
        ret = cursor

        if format == "lst":
            ret = list(ret)
        elif format == "class":
            ret = list(set([item["class"] for item in list(ret)]))
        elif format == "subclass":
            ret = [item["subclass_name"] for item in list(ret)]

        return ret

    def get_races(self, filter: dict = None, format: str = None):
        cursor = self.client[dbname][race_collection].find(filter)
        ret = cursor
        if format == "lst":
            ret = list(ret)
        elif format == "race":
            ret = list(set([item["race"] for item in list(ret)]))
        elif format == "subrace":
            ret = [item["subrace_name"] for item in list(ret)]
        return ret

    def get_class(self, class_name: str = None, subclass_name: str = None):
        if class_name is not None and subclass_name is not None:
            return self.client[dbname][class_collection].find_one(
                {"class": class_name, "subclass_name": subclass_name}
            )
        elif class_name is not None:
            return self.client[dbname][class_collection].find_one(
                {"class": class_name, "subclass_name": "None"}
            )

    def get_race(self, race_name: str = None, subrace_name: str = None):
        print(f"race is {race_name} , subrace is {subrace_name}")
        if race_name is not None and subrace_name is not None:
            return self.client[dbname][race_collection].find_one(
                {"race": race_name, "subrace_name": race_name}
            )
        elif race_name is not None:
            return self.client[dbname][race_collection].find_one({"race": race_name})

    def create_character(
        self,
        discord_channel,
        user_id,
        name,
        race_name,
        subrace_name,
        class_name,
        subclass_name,
        _str,
        _dex,
        _con,
        _int,
        _wis,
        _cha,
        asi1,
        asi2,
        asi3=None,
    ):
        valid_channels = ["registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"

        # TODO, check parameters are valid
        exists = self.get_character(name)
        if exists:
            return "character name already exists"

        asi1val = 1 if asi3 is None else 2
        asi2val = 1
        asi3val = 0 if asi3 is None else 1

        for asi in [(asi1, asi1val), (asi2, asi2val), (asi3, asi3val)]:
            target = None
            if asi[0] == "str":
                target = _str
            if asi[0] == "dex":
                target = _dex
            if asi[0] == "con":
                target = _con
            if asi[0] == "int":
                target = _int
            if asi[0] == "wis":
                target = _wis
            if asi[0] == "cha":
                target = _cha
            if target is not None:
                target += asi[1]

        data = {
            "Type": "Character",
            "Personaje": name,
            "Dueño": user_id,
            "XP": 0,
            "Fortuna": 0,
            "Prestigio": 0,
            "Evento": 0,
            "Chikievento": 0,
            "Descanso": 0,
            "GP": 50,
            "Level": 1,
            "Clases": f"{class_name}:{subclass_name}",
            "Race": f"{race_name}:{subrace_name}",
            "HP": 10 + (_con // 2 - 5),
            "FUE": _str,
            "DEX": _dex,
            "CON": _con,
            "INT": _int,
            "WIS": _wis,
            "CHA": _cha,
            "FEATS": "",
            "Stats de master": False,
            "Feat de Mastter": False,
        }

        self.insert_character(data)


if __name__ == "__main__":
    print("testing mongo connection")
    connector = mongo_connector()
    db = connector.client["d&d_server_main_db"]
    print(db)
    collection = db["test"]
    print(collection)
    pprint.pprint(connector.get_character("Glaurimm"))
