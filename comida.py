import os
import random
import typing

import pymongo
from pymongo import MongoClient

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.interactions import Interaction

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_server = os.getenv("MONGO_SERVER")

dbname = "d&d_server_main_db"
dbtable = "test_evento_comida"


class Conn:
    client = None

    def __init__(self):
        self.client = Conn.get_connect()

    def get_connect():
        connection_str = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_server}/?retryWrites=true&w=majority"
        client = MongoClient(connection_str)
        return client

    def comida(self, pts: int, dado: int, character_name=None, autor=None):
        cursor_player = self.client[dbname][dbtable].find_one(
            {"pj": character_name, "player": str(autor)}
        )

        if cursor_player is None:
            return -1

        total_pts = (
            pts
            if cursor_player.get("pts", None) is None
            else cursor_player["pts"] + pts
        )

        total_tiradas = (
            1
            if cursor_player.get("tiradas", None) is None
            else cursor_player["tiradas"] + 1
        )

        total_dado = (
            dado
            if cursor_player.get("dice", None) is None
            else cursor_player["dice"] + dado
        )

        self.client[dbname][dbtable].update_one(
            {"pj": character_name},
            {"$set": {"tiradas": total_tiradas}},
        )

        self.client[dbname][dbtable].update_one(
            {"pj": character_name},
            {"$set": {"pts": total_pts}},
        )

        self.client[dbname][dbtable].update_one(
            {"pj": character_name},
            {"$set": {"dice": total_dado}},
        )

        return total_pts

    def ranking(self):
        values = (
            self.client[dbname][dbtable]
            .find({"tiradas": {"$exists": True, "$not": {"$size": 0}}})
            .sort("pts", pymongo.ASCENDING)
        )

        resultados = []

        while values.alive:
            resultados.insert(0, values.next())

        return resultados


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
bd = Conn()


@bot.event
async def on_ready():
    print("Online")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@app_commands.guild_only()
class evento(app_commands.Group):
    # Declaración del comando para almacenaje en el Bot.Tree
    @app_commands.command(
        name="comidita", description="Usa un personaje para dar de comer al campamento"
    )
    # Descripción de los parametros que pide el comando
    @app_commands.describe(
        name="Nobre del personaje",
        mod="Modificador usado para la tirada",
        cause="Indica si tienes Outlander o alguna prof en herramientas",
    )
    # Decorator basado en cambiar el display name de los parametros
    @app_commands.rename(name="nombre", mod="modificador", cause="proficiencias")
    # Declaracion de la funcion que handlea el comando.
    async def comidita(
        self,
        interaction: discord.Interaction,
        name: str,
        mod: int,
        cause: typing.Optional[str] = "Nada",
    ):
        if (
            interaction.channel_id == 1201503427511992350
            or interaction.channel_id == 1173305500448858123
        ):
            dice = random.randint(1, 20)

            finalCause = (
                " al cual se le suma +5 por " + cause if cause != "Nada" else ""
            )

            total = dice + mod + 5 if cause != "Nada" else dice + mod

            pts = 3 if total > 20 else 2 if total >= 16 else 1 if total >= 11 else 0

            if cause in ["Nada", "Outlander", "Cook's Utensils", "Herbalist kit"]:
                flag = bd.comida(
                    pts=pts, dado=dice, character_name=name, autor=interaction.user.name
                )
            else:
                flag = -1

            if flag == -1:
                color = discord.Color.red()
                msg = "Error: Comprueba la ortografía o contacta con un programador (Llorar tambien es una opción)"
            else:
                color = discord.Color.yellow()
                msg = (
                    "Registro: "
                    + name
                    + " gasta 5 Días de Descanso en Trabajar en Supervivencia con un modificador de "
                    + str(mod)
                    + str(finalCause)
                    + "\n```  ____\n /\\' .\\    _____\n/: \\___\\  / .  /\\\n\\' / . / /____/..\\  "
                    + str(dice)
                    + " + "
                    + str(mod)
                    + (" + 5 " if cause != "Nada" else " ")
                    + "= "
                    + str(total)
                    + " \n \\/___/  \\'  '\\  /\n          \\'__'\\/```\n"
                    + str(name)
                    + " ha conseguido "
                    + str(pts)
                    + " pts. Llegando a un total de "
                    + str(flag)
                )

            embed = discord.Embed(description=msg, colour=color)

            embed.set_author(name="Evento comida")

            await interaction.response.send_message(embed=embed)

    @comidita.autocomplete("cause")
    async def drink_autocompletion(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for choices in ["Nada", "Outlander", "Cook's Utensils", "Herbalist kit"]:
            if current.lower() in choices.lower():
                data.append(app_commands.Choice(name=choices, value=choices))
        return data

    # Declaración del comando para almacenaje en el Bot.Tree
    @app_commands.command(
        name="ranking",
        description="Quieres ver los Rankings, no te preocupes este es tu comando.",
    )
    # Declaracion de la funcion que handlea el comando.
    async def ranking(self, interaction: discord.Interaction):
        if interaction.channel_id == 1173305500448858123 or interaction.channel_id == 1201503427511992350:
            stats = bd.ranking()

            min_luck = ["", 20]
            max_luck = ["", 0]
            max_salidas = ["", 0]
            total_pts = 0

            for data in stats:
                suerte = data["dice"] / data["tiradas"]
                if suerte < min_luck[1]:
                    min_luck = [data["pj"], suerte]

                if suerte > max_luck[1]:
                    max_luck = [data["pj"], suerte]

                if data["tiradas"] > max_salidas[1]:
                    max_salidas = [data["pj"], data["tiradas"]]

                total_pts = total_pts + data["pts"]
                
            color = discord.Color.dark_gold()

            embed = discord.Embed(
                description="╭═════════ .✧♛✧. ═════════╮\n|   ꧁༒♛- "
                + stats[0]["pj"]
                + " ["
                + str(stats[0]["pts"])
                + "pts] -♛༒꧂\n|\n|   ꧁༒☬ - "
                + stats[1]["pj"]
                + " ["
                + str(stats[1]["pts"])
                + "pts] - ☬༒꧂\n|\n|   ꧁༒• - "
                + stats[2]["pj"]
                + " ["
                + str(stats[2]["pts"])
                + "pts] - •༒꧂\n|\n|      \t—(••÷ "
                + stats[3]["pj"]
                + " ["
                + str(stats[3]["pts"])
                + "pts] ÷••)—\n|      —(••÷ "
                + stats[4]["pj"]
                + " ["
                + str(stats[4]["pts"])
                + "pts] ÷••)—\n|      —(••÷ "
                + stats[5]["pj"]
                + " ["
                + str(stats[5]["pts"])
                + "pts] ÷••)—\n|      —(••÷ "
                + stats[6]["pj"]
                + " ["
                + str(stats[6]["pts"])
                + "pts] ÷••)—\n╰═══ .Total del evento: ["
                + str(total_pts)
                + " pts] . ═══╯",
                colour=color,
            )

            embed.set_author(name="Ranking Evento")

            embed.add_field(
                name="Pj que peores dados:",
                value=(
                    min_luck[0] + " con una increible media de: " + str(min_luck[1])
                ),
                inline=False,
            )
            embed.add_field(
                name="Pj con mejores dados:",
                value=(
                    max_luck[0] + " con una increible media de: " + str(max_luck[1])
                ),
                inline=False,
            )
            embed.add_field(
                name="Pj que más días salió",
                value=(
                    max_salidas[0]
                    + " con un total de "
                    + str(max_salidas[1] * 5)
                    + " dias fuera"
                ),
                inline=False,
            )

            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1181152950945599590/1202268680654684161/450_1000.jpg?ex=65ccd6f6&is=65ba61f6&hm=0b10ceacdf60914bf533296730cd4daa20ac38de0820c7395efa377325c9f91e&"
            )

            await interaction.response.send_message(embed=embed)
        else:
            color = discord.Color.dark_gold()
            msg = "Eres un listillo tu no?\n ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⠁⠀⠙⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠶⣶⣿⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠏⠀⠀⠈⣿⠀⠀⠀⠀⠀⢸⣷⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢸⠇⠀⠀⠉⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢿⠇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠸⡷⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠋⠀⣾⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣧⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⣿⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⢹⡄⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠇⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀"

            embed = discord.Embed(description=msg, colour=color)

            embed.set_author(name="Listillo")

            await interaction.response.send_message(embed=embed, ephemeral=True)


bot.tree.clear_commands(guild=None)
bot.tree.add_command(evento())


bot.run(TOKEN)
