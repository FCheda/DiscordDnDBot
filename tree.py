import os

import discord
from discord.ext import commands
from discord import app_commands
import random
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
class interact(app_commands.Group):
    @app_commands.command()
    async def welcome(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Welcome, {interaction.user}!", ephemeral=True
        )

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


bot.tree.add_command(interact())

bot.run(TOKEN)
