import os
import typing

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.interactions import Interaction

import embedCreator as emb
import mongo_connector as mongo
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready():
    print("Online")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@app_commands.guild_only()
class personaje(app_commands.Group):
    
    # Declaración del comando para almacenaje en el Bot.Tree
    @app_commands.command(
        name="nuevo", description="Permite crear un personaje nuevo a un usuario"
    )
    # Descripción de los parametros que pide el comando
    @app_commands.describe(
        name="Nombre del nuevo personaje",
        race="Raza del nuevo personaje",
        subrace="Sub-raza del personaje en caso de tener",
        clase="Clase del nuevo personaje",
        subclase="Subclase del nuevo personaje en caso de tener una",
        fue="Fuerza del nuevo personaje, sin modificadores de raza",
        dex="Dextreza del nuevo personaje, sin modificadores de raza",
        con="Constitucion del nuevo personaje, sin modificadores de raza",
        inte="Inteligencia del nuevo personaje, sin modificadores de raza",
        wis="Sabiduría del nuevo personaje, sin modificadores de raza",
        cha="Carisma del nuevo personaje, sin modificadores de raza",
        asi1="Estadistica donde se aplica el modificador secundario de la raza",
        asi2="Estadistica donde se aplica el modificador secundario de la raza",
        asi3="Estadistica donde se aplica el modificador secundario de la raza",
    )
    # Decorator basado en cambiar el display name de los parametros
    @app_commands.rename(
        name="nombre",
        race="raza",
        subrace="sub-raza",
        clase="clase",
        subclase="sub-clase",
        fue="fuerza",
        dex="dextreza",
        con="constitución",
        inte="inteligencia",
        wis="sabiduría",
        cha="carisma",
        asi1="modificador_principal",
        asi2="modificador_secundario",
        asi3="modificador_terciario",
    )
    # Declaracion de la funcion que handlea el comando.
    async def nuevo(
        self,
        interaction: discord.Interaction,
        name: str,
        race: str,
        subrace: str,
        clase: str,
        subclase: Optional[str],
        fue: int,
        dex: int,
        con: int,
        inte: int,
        wis: int,
        cha: int,
        asi1: str,
        asi2: str,
        asi3: Optional[str],
    ):
        respuesta = mongo.mongo_connector.create_character(
            interaction.channel,
            interaction.user.id,
            name,
            race,
            subrace,
            clase,
            subclase,
            fue,
            dex,
            con,
            inte,
            wis,
            cha,
            asi1,
            asi2,
            asi3,
        )

        if respuesta:
            await interaction.response.send_message(
                embed=emb.template_generic(True, respuesta, interaction)
            )
        else:
            await interaction.response.send_message(
                embed=emb.template_generic(False, respuesta, interaction)
            )

    # Declaracion de las funciones de autocompletar
    @nuevo.autocomplete("raza")
    async def auto_race(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in mongo.mongo_connector.get_races(format="race"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    @nuevo.autocomplete("class")
    async def auto_race(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in mongo.mongo_connector.get_classes({}, "class"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    # Declaracion de funiones de autocompletar dependientes.
    @nuevo.autocomplete("sub-raza")
    async def auto_subrace(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        subrace = mongo.mongo_connector.get_races({"race":interaction.namespace.raza},format="subrace")
        for races in subrace:
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    @nuevo.autocomplete("sub-clase")
    async def auto_subrace(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        race = interaction.namespace.raza
        subraces = {
            "human": ["null"],
            "elf": ["Wood", "High", "Drow", "Eladrin"],
            "dwarf": ["Hill", "Mountain", "Fire"],
            "tieflin": ["1", "2", "3", "4", "5", "6"],
            "changelin": ["null"],
        }
        for races in subraces[race]:
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    # Comando para sacar informacion de un personaje
    @app_commands.command(
        name="info", description="Busca información sobre un personaje existente"
    )
    @app_commands.describe(name="Nombre del personaje")
    @app_commands.rename(
        name="nombre",
    )
    async def info(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(embed=emb.template_personaje(interaction, name))

    # Comando para subir de nivel un personaje.
    @app_commands.command(name="nivel", description="Sube de nivel a un personaje")
    @app_commands.describe(name="Nombre del persasonaje para subir de nivel")
    async def nivel(self, interaction: discord.Interaction, name: str):
        respuesta = mongo.mongo_connector #subir nivel 
       
        if respuesta == "":
            await interaction.response.send_message(
                embed=emb.template_generic(True, respuesta, interaction)
            )
        else:
            await interaction.response.send_message(
                embed=emb.template_generic(False, respuesta, interaction)
            ) 
        
    # Declaracion de las funciones de autocompletar nombre de pj dependiendo del jugador que interactue
    @nuevo.autocomplete("name")
    async def auto_name(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in mongo.mongo_connector.get_races({}, "race"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data
        


bot.tree.clear_commands(guild=None)
bot.tree.add_command(personaje())


bot.run(TOKEN)
