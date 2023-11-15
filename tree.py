import os

import discord
import random
import commands as logic
from discord.ext import commands
from discord import app_commands
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
    # Embed generico para enviarlo como mensaje al tener un canal erroneo.
    genEmbed = discord.Embed(
        title="Error",
        description="Canal incorrecto, el canal es #registros",
        colour=discord.Color.red(),
    )

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
        name="Nombre",
        race="Raza",
        subrace="Sub-Raza",
        clase="Clase",
        subclase="Sub-clase",
        fue="Fuerza",
        dex="Dextreza",
        con="Constitución",
        inte="Inteligencia",
        wis="Sabiduría",
        cha="Carisma",
        asi1="Modificador Principal",
        asi2="Modificador Secundario",
        asi3="Modificador Terciario",
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
        if interaction.channel_id == 1174044308417028197:
            
            await interaction.response.send_message(interaction.user.id)
        else:
            await interaction.response.send_message(embed=genEmbed, ephemeral=True)

    @app_commands.command()
    async def salute(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hello, {interaction.user}!", ephemeral=True
        )

    @app_commands.command()
    async def goodbye(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Bye bye, {interaction.user}!", ephemeral=True
        )


bot.tree.add_command(personaje())

bot.run(TOKEN)
