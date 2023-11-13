# bot.py
import os

import discord
from discord.ext import commands
import random
from dotenv import load_dotenv

# import data_query


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


@bot.tree.command(name="welcome")
async def welcome(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hello world, {interaction.user}!", ephemeral=True
    )


persData = {
    "id": "65516c22b8f97f0b07bab621",
    "name": "Glaurimm",
    "dueno": "Wheist",
    "lvl": 10,
    "xp": 63190,
    "oro": 14.67,
    "fort": 8,
    "prest": 13,
    "evento": 2,
    "clases": ["Warlock(Genie).9", "Clerigo.1"],
    "raza": "Genasi(water)",
    "hp": 70,
    "fue": 8,
    "dex": 13,
    "con": 16,
    "int": 12,
    "wis": 10,
    "cha": 18,
    "dias": 69,
    "asiMaster": False,
    "featMaster": True,
}


@bot.tree.command(name="personajeinfo")
async def personajeinfo(interation: discord.Interaction):
    persTemp = discord.Embed(
        title=persData["name"],
        description="Del usuario " + persData["dueno"],
        colour=0x00FF00,
    )
    persTemp.add_field(name="Raza:", value=persData["raza"])
    persTemp.add_field(name="Vida:", value=persData["hp"])
    persTemp.add_field(name="Exp:", value=persData["xp"])
    persTemp.add_field(
        name="Clases",
        value="\n".join(["- " + x for x in persData["clases"]]),
        inline=False,
    )
    persTemp.add_field(name="Fuerza:", value=persData["fue"])
    persTemp.add_field(name="Destreza:", value=persData["dex"])
    persTemp.add_field(name="Constitución:", value=persData["con"])
    persTemp.add_field(name="Inteligencia:", value=persData["int"])
    persTemp.add_field(name="Sabiduría:", value=persData["wis"])
    persTemp.add_field(name="Carisma:", value=persData["cha"])
    persTemp.add_field(
        name="Oro:",
        value=str(int(persData["oro"]))
        + " gp "
        + str(persData["oro"])[-2]
        + " sp "
        + str(persData["oro"])[-1]
        + " cp ",
        inline=False,
    )
    persTemp.add_field(name="Fortuna:", value=persData["fort"])
    persTemp.add_field(name="Prestigio:", value=persData["prest"])
    persTemp.add_field(name="", value="")
    persTemp.add_field(name="Evento:", value=persData["evento"])
    persTemp.add_field(name="Chikievento:", value=persData["evento"])
    persTemp.add_field(name="", value="")
    persTemp.add_field(name="Descanso:", value=persData["dias"])
    persTemp.add_field(name="Asi de master:", value="Usada" if persData["asiMaster"] else "No Usada")
    persTemp.add_field(name="Feat de master:", value="Usada" if persData["featMaster"] else "No Usada")
    await interation.response.send_message(embed=persTemp)


bot.run(TOKEN)
