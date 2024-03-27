import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint
import random
import validators
from bson.objectid import ObjectId
import copy
import datetime

load_dotenv()
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_server = os.getenv("MONGO_SERVER")

#
# PRO
dbname = "d&d_server_main_db"
character_collection = "characters"
player_collection = "players"
logs_collection = "log"
class_collection = "classes"
race_collection = "races"
market_collection = "mercado"
magic_items_collection = "magic_item_collection"
magic_items_tables = "magic_item_tables "

"""
# TEST
dbname = "d&d_server_main_db"
character_collection = "test"
player_collection = "test_player"
logs_collection = "test_log"
class_collection = "test_classes"
race_collection = "test_races"
market_collection = "test_mercado"
magic_items_collection = "test_magic_item_collection"
magic_items_tables = "test_magic_item_tables"
"""

XP_Dict = {
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000,
}


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

    def get_characters(self, filter: dict = None, format: str = None):
        cursor = self.client[dbname][character_collection].find(filter)
        ret = cursor
        if format == "lst":
            ret = list(ret)
        elif format == "name":
            ret = list(set([item["Personaje"] for item in list(ret)]))
        elif format == "level":
            ret = [item["Level"] for item in list(ret)]
        return ret

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

    def get_log(self, id: str):
        return self.client[dbname][logs_collection].find_one(ObjectId(id))

    def del_log(self, id: str):
        return self.client[dbname][logs_collection].find_one(ObjectId(id))

    def insert_log(self, dict=None):
        if dict is not None:
            id = self.client[dbname][logs_collection].insert(dict)
            return id
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

    def get_class(
        self, class_name: str = None, subclass_name: str = None, id: str = None
    ):
        if id is not None:
            return self.client[dbname][class_collection].find_one(ObjectId(id))
        if class_name is not None and subclass_name is not None:
            return self.client[dbname][class_collection].find_one(
                {"class": class_name, "subclass_name": subclass_name}
            )
        elif class_name is not None:
            return self.client[dbname][class_collection].find_one(
                {"class": class_name, "subclass_name": "None"}
            )

    def get_race(self, race_name: str = None, subrace_name: str = None, id: str = None):
        print(f"race is {race_name} , subrace is {subrace_name}")
        if id is not None:
            return self.client[dbname][race_collection].find_one(ObjectId(id))
        elif race_name is not None and subrace_name is not None:
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
            12: 4,
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
        new_player_dict = {
            "Nombre": player_id,
            "Fecha de creacion": {"$date": str(datetime.datetime.today())},
            "Rango GM": 0,
            "Max Pjs": 1,
            "Puntos GM": 0,
            "Partidas GM": 0,
            "Puntos Trabajo": 0,
            "Puntos Gastados": 0,
            "Dias GM": 0,
            "Dias Trabajo": 0,
            "Dias Gastados": 0,
            "Dias Reward (GM)": 0,
            "Puntos Reward (GM)": 0,
            "Evento Reward (GM)": 0,
            "Unlock GM": 0,
            "Unlock Trabajo": 0,
            "Unlock Totales": 0,
            "Tomos": 0,
            "Midas": 0,
            "Current Pjs": 0,
        }
        if self.get_player(player_id) is None:
            self.update_player(player_id, new_player_dict)
            return f"Created {player_id} data, wellcome!"
        else:
            return f"Error: {player_id} already exists!"

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
        valid_channels = ["✒-registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"

        db_race = self.get_race(race_name, subrace_name)
        if db_race is not None:
            print(f"selected raze is {db_race}")
        else:
            print("db_race is None")
            return "db_race is None"

        db_class = self.get_class(class_name, subclass_name)
        if db_class is not None:
            print(f"selected class is {db_class}")
        else:
            print("db_class is None")
            return "db_class is None"

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
            return "Asis are invalid"
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
            asi1val = 1
            asi2val = 1
            asi3val = 0

        if asi1 is None or str(asi1).lower() not in [
            "str",
            "dex",
            "con",
            "int",
            "wis",
            "cha",
        ]:
            return "ASI 1 erroneo"
        if asi2 is None or str(asi2).lower() not in [
            "str",
            "dex",
            "con",
            "int",
            "wis",
            "cha",
        ]:
            return "ASI 2 erroneo"

        for asi in [(asi1, asi1val), (asi2, asi2val), (asi3, asi3val)]:

            if str(asi[0]).lower() == "str":
                _str += asi[1]
            if str(asi[0]).lower() == "dex":
                _dex += asi[1]
            if str(asi[0]).lower() == "con":
                _con += asi[1]
            if str(asi[0]).lower() == "int":
                _int += asi[1]
            if str(asi[0]).lower() == "wis":
                _wis += asi[1]
            if str(asi[0]).lower() == "cha":
                _cha += asi[1]

        data = {
            "Type": "Character",
            "Personaje": name,
            "Dueño": user_id,
            "XP": 0,
            "Fortuna": 0.00,
            "Prestigio": 0.00,
            "Evento": 0,
            "Chikievento": 0,
            "Descanso": 0,
            "GP": 50.00,
            "Level": 1,
            "Classes": {
                str(
                    self.get_class(
                        class_name=class_name, subclass_name=subclass_name
                    ).get("_id")
                ): 1
            },
            "Race": str(
                self.get_race(race_name=race_name, subrace_name=subrace_name).get("_id")
            ),
            "HP": base_hp + (_con // 2 - 5),
            "FUE": _str,
            "DEX": _dex,
            "CON": _con,
            "INT": _int,
            "WIS": _wis,
            "CHA": _cha,
            "FEATS": "",
            "Unused Feats": _free_feats,
            "Feats": {},
            "Rewards": [],
        }

        result = self.insert_character(data)
        result2 = self.update_player(
            user_id, {"Current Pjs": player.get("Current Pjs", 0) + 1}
        )

        return (result, result2)  # TODO retornar None a la interfaz si funciono.

    def level_up(
        self,
        discord_channel,
        user_id,  # id discord
        name,
        class_name=None,
        subclass_name=None,
        life_method_roll=None,
    ):
        # Ej: level_up("registros","arctic8411","Elizabeth")
        valid_channels = ["✒-registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"
        character = self.get_character(name)
        player = self.get_player(user_id)
        if player is None:
            return "Player is none"
        if character is None:
            return "Character is none"
        if character.get("Dueño") != user_id:
            return f"El personaje {name} no pertenece a {user_id}"
        # check level
        if XP_Dict[int(character.get("Level")) + 1] > int(character.get("XP")):
            return f"{name} no tiene suficiente XP para subir de nivel: tiene {int(character.get('XP'))} y necesita {XP_Dict[int(character.get('Level')) + 1]}"
        # check class
        replace_class = None
        character_class = self.get_class(id=list(character.get("Classes").keys())[0])
        number_of_lvls_to_mod = 1
        if class_name is not None:
            for class_id, levels in character.get("Classes").items():
                this_class = self.get_class(id=class_id)
                if class_name == this_class.get("class"):
                    # we already have the class
                    if levels + 1 == this_class.get("subclass_level"):
                        # set subclass
                        if subclass_name is not None:
                            character_class = self.get_class(class_name, subclass_name)
                            replace_class = this_class
                            if this_class.get("hp_mod") != character_class.get(
                                "hp_mod"
                            ):
                                number_of_lvls_to_mod = this_class.get("subclass_level")
                            break
                        else:
                            return f"Yo need to specify subclass for {class_name} at class lvl {levels+1}"
                    else:
                        character_class = this_class
                        break
        else:
            levels = list(character.get("Classes").values())[0]
            if character_class.get("subclass_level") == levels + 1:
                return f"Yo need to specify subclass for {class_name} at class lvl {levels+1}"
        # get lif
        life_increase = 0
        if life_method_roll != None:
            life_increase = (
                random.randint(1, character_class["hp_dice"])
                + character_class["hp_mod"] * number_of_lvls_to_mod
                + (character["CON"] - 10) // 2 * 1
                + self.get_race(id=character.get("Race")).get("hp_mod")
            )
        else:
            life_increase = (
                character_class["hp_dice"] // 2
                + 1
                + character_class["hp_mod"] * number_of_lvls_to_mod
                + (character["CON"] - 10) // 2 * 1
                + self.get_race(id=character.get("Race")).get("hp_mod")
            )

        # replace class, and set new level
        add_feat = False
        level = None
        if replace_class != None:
            level = character["Classes"][str(replace_class.get("_id"))] + 1
            character["Classes"].pop(str(replace_class.get("_id")), None)
            character["Classes"][str(character_class.get("_id"))] = level
        else:
            level = character["Classes"][str(character_class.get("_id"))] + 1
            character["Classes"][str(character_class.get("_id"))] = level
        if level in [4, 8, 12, 16, 19] or (
            class_name == "Fighter" and level in [6, 12, 14]
        ):
            add_feat = True

        character["HP"] = character["HP"] + life_increase
        character["Level"] = character["Level"] + 1
        if add_feat:
            character["unused_feat"] = character.get("unused_feat") + 1
        else:
            character["unused_feat"] = character.get("unused_feat", 0)

        update_dict = {
            "HP": character["HP"],
            "Level": character["Level"],
            "unused_feat": character["unused_feat"],
            "Classes": character["Classes"],
        }
        self.update_character(name, update_dict)
        return "Success"

    def set_subclass():
        # TODO
        pass

    def set_feat():
        # TODO
        pass

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

    def get_gm_update_dict(self, player, rewards, reverse=False):
        foo = self.get_player(player)
        multiplier = 1
        if reverse:
            multiplier = -1
        for key in rewards.keys():
            rewards[key] = rewards[key] * multiplier + foo.get(key, 0)
        return rewards

    def store_log_in_db(self, player_rewards, gm, gm_rewards):
        log_checkpoint = {
            "gm": gm,
            "player_rewards": player_rewards,
            "gm_rewards": gm_rewards,
        }

        id = self.insert_log(log_checkpoint)
        return id

    def process_log(self, channel, gm, log):
        """

        example: process_log("logs","Kana",log)
        """
        valid_channels = ["📒-logs", "bot_log_tests"]
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
        # print(log_dict[player])
        for index, line in enumerate(lines[3:]):
            if line[: len("Especial:")] == "Especial:":
                tokens = [x.strip() for x in line[len("Especial:") :].split(",")]
                limit = 5
                if "Evento" and "Chikievento" in line:
                    limit = 7
                elif "evento" or "Chikievento" in line:
                    limit = 6
                special_players = tokens[:-limit]
                special_rewards = [token.split(" ")[0] for token in tokens[-limit:]]
                for player in special_players:
                    if player not in log_dict:
                        message = f"{gm} cabrón, no me jodas el bot -> especial {player} NO esta en la lista de jugadores"
                        print(message)
                        return message
                    else:
                        print(f"DEBUG player special rewards {special_rewards}")
                        log_dict[player] = self.get_player_log_rewards(special_rewards)
        print("initial log dict line 450")
        store_log_dict = copy.deepcopy(log_dict)  # to store a cold copy
        for character, rewards in log_dict.items():
            update_rewards = self.get_character_update_dict(character, rewards)
            self.update_character(character, update_rewards)
        # master rewards
        gm_rewards = self.get_gm_update_dict(gm, self.get_gm_rewards(base_rewards))
        self.update_player(gm, gm_rewards)

        log_checkpoint = self.store_log_in_db(
            store_log_dict, gm, self.get_gm_rewards(base_rewards)
        )

        message = "log succesfull \n" + str(log_checkpoint)

        # TODO, add insert the full log in a new table

        return message

    def get_log_by_id(self, channel, log_id):
        if channel in ["bot-test", "oficina"]:
            return self.get_log(log_id)
        else:
            return "invalid channel"

    def undo_log_by_id(self, channel, log_id):
        if channel in ["superadmin"]:
            log = self.get_log(log_id)
            gm_rewards = self.get_gm_update_dict(
                log["gm"], log["gm_rewards"], reverse=True
            )
            self.update_player(log["gm"], gm_rewards)
            for character, rewards in log["player_rewards"].items():
                update_rewards = self.get_character_update_dict(
                    character, rewards, reverse=True
                )
                self.update_character(character, update_rewards)
            self.del_log(log_id)
            return f"log {log_id} undone"
        else:
            return "invalid channel"

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

    # ROLL ITEM TABLES

    def get_magic_table_definition(self, table_name):
        return self.client[dbname][magic_items_tables].find_one({"table": table_name})

    def get_magic_table_items(self, table_name, format):
        cursor = self.client[dbname][magic_items_collection].find({"table": table_name})
        if format == "lst":
            return list(cursor)
        return cursor

    def get_magic_table_item(self, item):
        return self.client[dbname][magic_items_collection].find_one({"item": item})

    def roll_magic_item_table(self, discord_channel, user_id, name, table_name):
        valid_channels = ["registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"
        character = self.get_character(name)
        player = self.get_player(user_id)
        if player is None:
            return "Player is none"
        if character is None:
            return "Character is none"
        if character.get("Dueño") != user_id:
            return f"El personaje {name} no pertenece a {user_id}"

        table = self.get_magic_table_definition(table_name)
        if table is None:
            return f"Table {table_name} not found"
        table_cost = table.get("cost")
        table_items = self.get_magic_table_items(table_name, format="lst")

        if character["Fortuna"] < table_cost:
            return f"{character['Personaje']} no tiene suficiente fortuna"

        roll = random.randint(0, len(table_items) - 1)

        self.update_character(
            character["Personaje"],
            self.get_character_update_dict(
                character["Personaje"], {"Fortuna": table_cost}, reverse=True
            ),
        )

        return f"{character['Personaje']} ha tirado en la tabla {table_name}, recibiendo   ---->  {table_items[roll]['item']}"

    def roll_magic_custom_table(self, discord_channel, user_id, name, item_list):
        coste_prestigio = 5
        valid_channels = ["registros", "bot-test"]
        if discord_channel not in valid_channels:
            return "channel is not valid"
        character = self.get_character(name)
        player = self.get_player(user_id)
        if player is None:
            return "Player is none"
        if character is None:
            return "Character is none"
        if character.get("Dueño") != user_id:
            return f"El personaje {name} no pertenece a {user_id}"

        # get items and fortune cost
        print(item_list)

        tables = []
        items = []
        fortune_costs = []
        if len(item_list) != len(set(item_list)):
            return "No se puede incluir varias veces el mismo objeto"

        for item in item_list:
            foo = self.get_magic_table_item(item)
            if foo is None:
                return f"{item} no existe"
            items.append(foo["item"])
            tables.append(foo["table"])
            fortune_costs.append(
                self.get_magic_table_definition(foo["table"]).get("cost", 0)
            )

        if character["Prestigio"] < coste_prestigio:
            return f"{character['Personaje']} no tiene suficiente prestigio"
        if character["Fortuna"] < max(fortune_costs):
            return f"{character['Personaje']} no tiene suficiente fortuna"
        # roll
        roll = random.randint(0, len(items) - 1)
        # update character
        self.update_character(
            character["Personaje"],
            self.get_character_update_dict(
                character["Personaje"],
                {"Fortuna": max(fortune_costs), "Prestigio": coste_prestigio},
                reverse=True,
            ),
        )
        # write message
        result = f"{name} ha tirado en una tabla personalizada pagando {coste_prestigio} Prestigio y {max(fortune_costs)} Fortuna, obteniendo -> {items[roll]}"

        return result


if __name__ == "__main__":
    print("testing mongo connection")
    connector = mongo_connector()
    db = connector.client["d&d_server_main_db"]
    print(db)
    collection = db["test"]
    print(collection)
    pprint.pprint(connector.get_character("Glaurimm"))
