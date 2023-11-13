# bot.py
import os
import sys
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random
from dotenv import load_dotenv
import data_query


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


data_querier = data_query.dnddata()


intents = discord.Intents.default()
intents.message_content = True

"""
class CustomClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
"""

# bot command tests
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command(name="test")
async def _test(ctx, arg1, arg2):
    embed = discord.Embed(
        title="Test command",
        description=f" You sended:\n arg1: {arg1} \n arg2: {arg2} \n This is an embeded response",
        color=0x00FF00,
    )
    embed.add_field(name="Esto es un field con titulo", value="Valor del field")
    embed.add_field(name="Otro field", value="Valor del otro field")
    await ctx.send(embed=embed)


@bot.tree.command(name="tree_test")
async def _tree_test(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hello word, {interaction.user.guild}!", ephemeral=True
    )


@bot.tree.command(name="drink")
async def drink(interaction: discord.Interaction, item: str):
    await interaction.response.send_message(
        f"{item}, {interaction.user}!", ephemeral=True
    )


@drink.autocomplete("item")
async def drink_autocompletion(
    interaction: discord.Interaction, current: str
) -> typing.List[app_commands.Choice[str]]:
    data = []
    for drink_choice in ["beer", "blood", "tea", "coffe"]:
        if current.lower() in drink_choice.lower():
            data.append(app_commands.Choice(name=drink_choice, value=drink_choice))
    return data


@bot.event
async def on_ready():
    print("online")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# bot general tests
client = discord.Client(intents=intents)


bot_channels = ["bot-test"]


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    # members = "\n - ".join([member.name for member in guild.members])
    # print(f"Guild Members:\n - {members}")


@client.event
async def on_message(message):
    print("got message")
    print(f"Author: {message.author.name}")
    print(f"Channel: {message.channel.name}")
    print(f"Content: {message.content}")
    print(f"Clean_Content: {message.clean_content}")
    print(f"System_Content: {message.system_content}")

    if message.channel.name not in bot_channels:
        return

    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        "I'm the human form of the 💯 emoji",
        "Bingpot!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
        ),
    ]

    sex_quotes = [
        "Venga ponte, que te lo como todo",
        "I want to f**k you so bad right now...",
        "You would probably sleep better if we had sex.",
        "I liked it so its mine UwU",
    ]

    if message.content == "99!":
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    if message.content == "69!":
        response = random.choice(sex_quotes)
        await message.channel.send(response)

    commands = ["!get character ", "!get player "]

    if commands[0] in str(message.content):
        # response = "character query: " + message.content[len(commands[0]) :]
        response = data_querier.get_query(query=message.content[len(commands[0]) :])
        await message.channel.send(response)
    if commands[1] in str(message.content):
        # response = "character query: " + message.content[len(commands[0]) :]
        response = data_querier.get_query(
            type="player", query=message.content[len(commands[1]) :]
        )
        await message.channel.send(response)
    # if message.content == "Que piensas de Fedor?":
    #    response = "Ufff esta buenorro el tio pero lo tiene pillado ems :("
    #    await message.channel.send(response)


# client.run(TOKEN)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-cli":
            print("starting as client")
            client.run(TOKEN)

        elif sys.argv[1] == "-bot":
            print("starting as bot")
            bot.run(TOKEN)
    else:
        print(
            """
      Usage
      
      missing command -bot or -cli
      
      """
        )
