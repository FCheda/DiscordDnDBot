import discord
from discord.ext import commands


class commands:
    bot = None
    intents = None

    def __init__(self, bot=None, intents=None):
        if intents is None:
            self.intents = intents = discord.Intents.default()
        if bot is None:
            self.bot = commands.Bot(command_prefix="$", intents=intents)

        pass
    def _init_commands(self):
      