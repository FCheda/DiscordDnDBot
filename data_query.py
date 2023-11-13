import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
sheet_id = os.getenv("SHEET_ID")
sheet_characters = os.getenv("SHEET_CHARACTER_NAME")
sheet_players = os.getenv("SHEET_PLAYERS_NAME")
sheet_characters_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_characters}"
sheet_players_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_players}"


class dnddata:
    char_data = None
    player_data = None

    def __init__(self):
        self.char_data = dnddata.get_data()
        self.player_data = dnddata.get_data(sheet_players_url)

    def get_data(url=sheet_characters_url):
        return pd.read_csv(url)

    def get_connection():
        pass

    def get_query(self, type="char", query="Ejemplo"):
        if type == "char":
            return str(
                self.char_data[self.char_data["Personaje"] == query].to_dict("records")[
                    0
                ]
            )
        elif type == "player":
            return str(
                self.player_data[self.player_data["Nombre"] == query].to_dict(
                    "records"
                )[0]
            )
        else:
            return "not supported"


if __name__ == "__main__":
    foo = dnddata()
    print(foo.get_query(query="Elizabeth"))
