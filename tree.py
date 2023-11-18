import os

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.interactions import Interaction

import mongo_connector as logic
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




class Modal(ui.Modal, title="Cesta de la compra:"):
    name = ui.TextInput(label="Nombre del personaje:")
    answer = ui.TextInput(label="Compra:",placeholder="- 1 Boat\n- 1 Fine Wine" ,style=discord.TextStyle.paragraph)
    
    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f"Gracias por participar en esta encuesta, {self.name}!")

@app_commands.guild_only()
class personaje(app_commands.Group):
        # Declaración del comando para almacenaje en el Bot.Tree
    @app_commands.command(
        name="crear", description="Permite crear un personaje nuevo a un usuario"
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
    async def crear(
        self,
        interaction: discord.Interaction,
        name: str,
        race: str,
        subrace: Optional[str],
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
        await interaction.response.send_message(name)
        """ logic.mongo_connector.create_character(
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
            asi3
        ) """

    @app_commands.command()
    async def salute(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Modal())

    @app_commands.command()
    async def goodbye(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Bye bye, {interaction.user}!", ephemeral=True
        )


bot.tree.add_command(personaje())

bot.run(TOKEN)
