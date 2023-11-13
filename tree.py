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


@bot.tree.command(name="Hello world")
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
    "asiMaster": False,
    "featMaster": True,
}


@bot.tree.command(name="personaje_info")
async def personaje_info():
    persTemp = discord.Embed(
        title=persData["name"],
        description="Del usuario " + persData["dueno"],
        colour=800080,
    )
    persTemp.add_field(name = "Raza:", value = persData["raza"])
    persTemp.add_field(name = "Vida:", value = persData["hp"])
    persTemp.add_field(name = "Exp:", value = persData["xp"])
    persTemp.add_field(name = "Clases", value = persData["clases"])


bot.run(TOKEN)
