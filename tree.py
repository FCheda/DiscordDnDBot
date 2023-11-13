# bot.py
import os

import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
#import data_query


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!", intents= discord.Intents.default())

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
    await interaction.response.send_message(f"Hello world, {interaction.user.guild}!", ephemeral=True)

bot.run(TOKEN)