import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint
import random
import validators

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
market_collection = "test_mercado"
magic_items_collection = "test_magic_item_tables"


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

    def set_character_url(self, character, player, url):
        char = self.get_character(character)
        if player != char["Dueño"]:
            return f"{player} no tiene ningun personaje llamado {character}"

        if url is not None and validators.url(url):
            self.update_character(character, {"image_url": url})
            return "Success"
        elif url is not None:
            print("!!!!! url badly formed")

    def update_player(self, player_name=None, dict=None):
        print(f"updating player {player_name}")
        if player_name is not None:
            if dict is not None:
                newvalues = {"$set": dict}
                result = self.client[dbname][player_collection].update_one(
                    {"Nombre": player_name}, newvalues
                )
            else:
                newvalues = {"$set": {"rabo": f"{random.randint(0,20)} cm"}}
                result = self.client[dbname][player_collection].update_one(
                    {"Nombre": player_name}, newvalues
                )
        return result

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
                {"race": race_name, "subrace_name": subrace_name}
            )
        elif race_name is not None:
            return self.client[dbname][race_collection].find_one({"race": race_name})

    def get_point_cost(self, asi):
        point_cost = {
            8: 0,
            9: 1,
            10: 2,
            11: 3,
            12: 3,
            13: 5,
            14: 7,
            15: 9,
        }
        return point_cost.get(asi, None)

    def navidad(self, character_name=None, autor=None):
        cursor_player = self.client[dbname]["test_navidad"].find_one(
            {"pj": character_name, "player": str(autor)}
        )
        if cursor_player is None:
            return f"{str(autor)} no tiene ningun personaje llamado {character_name}"
        # cursor_regalos = self.client[dbname]["test_navidad_regalos"].find(filter)
        if cursor_player.get("regalo", None) is not None:
            return "solo 1 regalo por cabeza"

        print(type(cursor_player))
        pprint.pprint(cursor_player)

        regalo = ["nombre_regalo", "descripcion_regalo"]

        roll = random.randint(1, 20)

        if character_name == "Test":
            roll = 25

        cursor_regalos = self.client[dbname]["test_navidad_regalos"].find_one(
            {"roll": roll}
        )

        if cursor_regalos is not None:
            regalo[0] = cursor_regalos["item"]
            regalo[1] = cursor_regalos["description"]
        else:
            return "Algo extraño ha pasado, regalo no encontrado"

        print("updating char...")
        self.client[dbname]["test_navidad"].update_one(
            {"pj": character_name}, {"$set": {"regalo": regalo[0]}}
        )

        # return "hiden test"

        print("Message autor is: " + str(autor))
        result = f"{character_name} ha abierto su regalo y ha encontrado: {regalo[0]} !!! \n {regalo[1]}"
        print(result)
        return result

    def check_point_buy(self, asis):
        points = [self.get_point_cost(asi) for asi in asis]
        if None not in points and sum(points) == 27:
            return True
        return False

    def create_player(self, player_id: str):
        pass

    def create_character(
        self,
        discord_channel,
        user_id,  # id discord
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
        """example = connector.create_character("registros","test","pika2","Dragonborn","Metalic","Artificer","Alchemist",15,15,15,8,8,8,"str","dex")"""
        valid_channels = ["registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"

        db_race = self.get_race(race_name, subrace_name)
        if db_race is not None:
            print(f"selected raze is {db_race}")
        else:
            print("db_race is None")
            return None

        db_class = self.get_class(class_name, subclass_name)
        if db_class is not None:
            print(f"selected class is {db_class}")
        else:
            print("db_class is None")
            return None

        player = self.get_player(user_id)
        if player is None:
            self.create_player(user_id)
            player = self.get_player(user_id)

        if player.get("Current Pjs", 0) >= player.get("Max Pjs", 0):
            return f"Max Pjs Reached, Current {player.get('Current Pjs',0)}, Max {player.get('Max Pjs',0)}"

        exists = self.get_character(name)
        if exists:
            return "character name already exists"

        if (
            self.check_point_buy(
                [
                    _str,
                    _dex,
                    _con,
                    _int,
                    _wis,
                    _cha,
                ]
            )
            is False
        ):
            return (None, "Asis are invalid")
        base_hp = db_class["hp_dice"] + db_class["hp_mod"] + db_race["hp_mod"]
        _free_feats = 0
        print(f"free feat is {db_race.get('free_feat',None)}")
        if db_race.get("free_feat", None) is True:
            print("adding free feat")
            _free_feats = 1

        if _free_feats == 0:
            asi1val = 1 if asi3 is None else 2
            asi2val = 1
            asi3val = 0 if asi3 is None else 1
        else:
            asi1val = 1 if asi2 is None else 2
            asi2val = 0 if asi2 is None else 1
            asi3val = 0

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
            "Clases": ({"class": class_name, "subclass": subclass_name, "lvl": 1}),
            "Race": {"race": race_name, "subrace": subrace_name},
            "HP": base_hp + (_con // 2 - 5),
            "FUE": _str,
            "DEX": _dex,
            "CON": _con,
            "INT": _int,
            "WIS": _wis,
            "CHA": _cha,
            "FEATS": "",
            "Unused Feats": _free_feats,
            "Stats de master": False,
            "Feat de Mastter": False,
        }

        result = self.insert_character(data)
        result2 = self.update_player(
            user_id, {"Current Pjs": player.get("Current Pjs", 0) + 1}
        )

        return (result, result2)  # TODO retornar None a la interfaz si funciono.

    ##logs
    def get_player_log_rewards(self, base_rewards):
        # TODO: cambar para que reciba las tuplas separadas por espacio y asigne a cada valor  sin importar posicion
        print(base_rewards)
        while len(base_rewards) < 7:
            base_rewards.append(0)
        dict = {
            "XP": int(base_rewards[0]),
            "Descanso": int(base_rewards[1]),
            "GP": float(base_rewards[2]),
            "Fortuna": int(base_rewards[3]),
            "Prestigio": float(base_rewards[4]),
            "Evento": float(base_rewards[5]),
            "Chiquievento": float(base_rewards[6]),
        }
        return dict

    def get_character_update_dict(self, character, rewards, reverse=False):
        foo = self.get_character(character)
        for key in rewards.keys():
            if reverse is False:
                rewards[key] = rewards[key] + foo.get(key, 0)
            else:
                rewards[key] = foo.get(key, 0) - rewards[key]
                if rewards[key] < 0:
                    return None
        return rewards

    def get_gm_rewards(self, base_rewards):
        dict = {
            "Dias GM": int(base_rewards[1]),
            "Puntos GM": 3,
            "Partidas GM": 1,
        }
        return dict

    def get_gm_update_dict(self, player, rewards):
        foo = self.get_player(player)
        for key in rewards.keys():
            rewards[key] = rewards[key] + foo.get(key, 0)
        return rewards

    def process_log(self, channel, gm, log):
        """

        example: process_log("logs","Kana",log)
        """
        valid_channels = ["log", "bot_log_tests"]
        if channel not in valid_channels:
            message = "Log has not been processed, wrong channel"
            return message

        lines = log.split("\n")
        log_dict = {}
        base_rewards = []
        base_players = []

        lines = [line for line in lines if line != ""]
        if len(lines) < 3:
            return "At least 2 lines are required"
        if self.get_player(gm) is None:
            return "invalid player/gm"
        for index, line in enumerate(lines[:3]):
            # print(index,line)
            if index == 1:
                base_rewards = [
                    i.strip().split(" ")[0]
                    for i in line[len("Recompensas:") :].split(",")
                ]
            if index == 2:
                base_players = [
                    i.strip() for i in line[len("Participantes:") :].split(",")
                ]

        for player in base_players:
            log_dict[player] = self.get_player_log_rewards(base_rewards)
        for index, line in enumerate(lines[3:]):
            if line[: len("Especial:")] == "Especial:":
                tokens = [x.strip() for x in line[len("Especial:") :].split(",")]
                special_players = tokens[:-5]
                special_rewards = [token.split(" ")[0] for token in tokens[-5:]]
                for player in special_players:
                    if player not in log_dict:
                        message = f"{gm} cabrón, no me jodas el bot -> especial {player} NO esta en la lista de jugadores"
                        print(message)
                        return message
                    else:
                        log_dict[player] = self.get_player_log_rewards(special_rewards)

        for character, rewards in log_dict.items():
            update_rewards = self.get_character_update_dict(character, rewards)
            self.update_character(character, update_rewards)
        # master rewards
        gm_rewards = self.get_gm_update_dict(gm, self.get_gm_rewards(base_rewards))
        self.update_player(gm, gm_rewards)

        pprint.pprint(log_dict)
        pprint.pprint(gm_rewards)
        message = "log succesfull"

        # TODO, add insert the full log in a new table

        return message

    # buy items
    def get_item(self, item_name):
        if item_name is not None:
            return self.client[dbname][market_collection].find_one(
                {"Nombre": item_name}
            )

    def get_items_cost(self, items_dict, sell):
        cost = {}
        mult = 1
        if sell:
            mult = -0.5

        for item_name in items_dict.keys():
            item = self.get_item(item_name)
            if item is None:
                return None
            elif item.get("Disponible", None) != "SI":
                return None
            cost["GP"] = (
                cost.get("GP", 0) + item.get("Precio", 0) * items_dict[item_name] * mult
            )
            cost["Fortuna"] = (
                cost.get("Fortuna", 0)
                + item.get("Fortuna", 0) * items_dict[item_name] * mult
            )
            cost["Prestigio"] = (
                cost.get("Prestigio", 0)
                + item.get("Prestigio", 0) * items_dict[item_name] * mult
            )

        return cost

    def buy_or_sell_items(self, author, text):
        lines = text.split("\n")
        character = None
        buy_dict = {}
        sell = False
        lines = [line for line in lines if line != ""]
        for id, line in enumerate(lines):
            if id == 0:
                if "compra" in line[-(len(" compra:")) :]:
                    character_name = line[: -(len(" compra:"))]
                elif "vende" in line[-(len(" vende:")) :]:
                    character_name = line[: -(len(" vende:"))]
                    sell = True
                character = self.get_character(character_name)
                if character is not None and character.get("Dueño") != author:
                    message = f"Error: {author} no tiene ningun personaje llamado {character_name}"
                    return message
            else:
                split_line = line.split(" ")
                buy_dict[" ".join(split_line[2:])] = int(split_line[1])
        cost = self.get_items_cost(buy_dict, sell)
        if cost is None:
            message = "Error: Alguno de los objetos solicitados no esta disponible"
            return message
        update_dict = self.get_character_update_dict(
            character.get("Personaje", None), cost, reverse=True
        )
        if update_dict is None:
            message = "Error: No tienes suficientes recursos para pagar esa compra "
            return message
        result = self.update_character(character.get("Personaje", None), update_dict)
        message = "Success"
        return message


if __name__ == "__main__":
    print("testing mongo connection")
    connector = mongo_connector()
    db = connector.client["d&d_server_main_db"]
    print(db)
    collection = db["test"]
    print(collection)
    pprint.pprint(connector.get_character("Glaurimm"))
