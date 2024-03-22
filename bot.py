# bot.py
import os
import sys
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random
from dotenv import load_dotenv  #
from typing import Optional
import mongo_connector

import custom_commands


connector = mongo_connector.mongo_connector()


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


intents = discord.Intents.default()
intents.message_content = True

"""
class CustomClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
"""
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

"""
# bot general tests
bot = commands.Bot(command_prefix="/", intents=intents)


bot_channels = [
    "bot-test",
    "sorpresas-navideñas",
    "recompensas",
    "bot_log_tests",
    "bot_compras_tests",
    "consultas",
    "✒-registros",
    "📒-logs",
]


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    # sync commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    # members = "\n - ".join([member.name for member in guild.members])
    # print(f"Guild Members:\n - {members}")


@bot.event
async def on_message(message):
    print("got message")
    print(f"Author: {message.author.name}")
    print(f"Channel: {message.channel.name}")
    print(f"Content: {message.content}")
    print(f"Clean_Content: {message.clean_content}")
    print(f"System_Content: {message.system_content}")

    if message.channel.name not in bot_channels:
        print("invalid channel")
        return

    if message.author == bot.user:
        print("bad author")
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

    # listeners
    if message.content == "99!":
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    if message.content == "69!":
        response = random.choice(sex_quotes)
        await message.channel.send(response)
    if (
        str(message.channel) == "bot_log_tests"
    ):  # and message.author.id != "D&D Bot#5178":
        # response = random.choice(sex_quotes)
        # await message.channel.send(response)
        # print("GOT LOG !!! PROCESSING")

        response = connector.process_log(
            str(message.channel), str(message.author.name), str(message.content)
        )
        print(response)
        await message.channel.send(response)
    if (
        str(message.channel) == "bot_compras_tests"
    ):  # and message.author.id != "D&D Bot#5178":
        # response = random.choice(sex_quotes)
        # await message.channel.send(response)
        # print("GOT LOG !!! PROCESSING")

        response = connector.buy_or_sell_items(
            str(message.author.name), str(message.content)
        )
        print(response)
        await message.channel.send(response)

    # commands

    commands = [
        "!get character ",
        "!get player ",
        "!update character ",
        "!player character ",
        "!insert log ",
        "!get class ",
        "!get race ",
        "!get classes ",
        "!get races ",
        "!navidad ",
        "!update_character_url ",
        "!get log ",
        "!undo log ",
        "!registro jugador",
        "!tabla tirar ",
        "!tabla custom ",
    ]

    if commands[0] in str(message.content):
        # response = "character query: " + message.content[len(commands[0]) :]
        # embed = custom_commands.personajeinfo(connector, None, None, message.content[len(commands[0]) :])
        embed = custom_commands.template_personaje(
            connector, message.channel.name, message.content[len(commands[0]) :]
        )
        # response = connector.get_character(message.content[len(commands[0]) :])
        # embed = discord.Embed(title="Title", description="Desc", color=0x00FF00)
        if type(embed) == str:
            await message.channel.send(str(embed))
            embed = None
        if embed is not None:
            await message.channel.send(embed=embed)
        # await interationresponse.send_message(embed=persTemp)
    if commands[1] in str(message.content):
        response = connector.get_player(message.content[len(commands[1]) :])
        await message.channel.send(response)
    if commands[2] in str(message.content):
        response = connector.update_character(
            message.content[len(commands[2]) :],
        )
        await message.channel.send(str(response))
    if commands[3] in str(message.content):
        response = connector.update_player(
            message.content[len(commands[3]) :],
        )
        await message.channel.send(str(response))
    if commands[4] in str(message.content):
        response = connector.insert_log(
            message.content[len(commands[4]) :],
        )
        await message.channel.send(str(response))
    if commands[5] in str(message.content):
        response = connector.get_class(
            class_name=message.content[len(commands[5]) :],
        )
        await message.channel.send(str(response))
    if commands[6] in str(message.content):
        response = connector.get_race(
            race_name=message.content[len(commands[6]) :],
        )
        await message.channel.send(str(response))
    if commands[7] in str(message.content):
        response = connector.get_races(message.content[len(commands[6]) :], "races")
        await message.channel.send(str(response))
    if commands[8] in str(message.content):
        response = connector.get_race(message.content[len(commands[6]) :], "classes")
        await message.channel.send(str(response))
    if commands[9] in str(message.content):
        response = connector.navidad(
            message.content[len(commands[9]) :], message.author.name
        )
        await message.channel.send(str(response))
    if commands[10] in str(message.content):
        split = message.content.split(" ")
        response = connector.set_character_url(
            " ".join(split[1:-1]), str(message.author.name), split[-1]
        )
        await message.channel.send(str(response))
    if commands[11] in str(message.content):
        response = connector.get_log_by_id(
            message.channel.name,
            message.content[len(commands[11]) :],
        )
        await message.channel.send(str(response))
    if commands[12] in str(message.content):
        response = connector.undo_log_by_id(
            message.channel.name,
            message.content[len(commands[12]) :],
        )
        await message.channel.send(str(response))
    if commands[13] in str(message.content):
        response = connector.create_player(str(message.author.name))
        await message.channel.send(str(response))
    if commands[14] in str(message.content):
        response = connector.roll_magic_item_table(
            discord_channel=message.channel.name,
            user_id=str(message.author.name),
            name=message.content[len(commands[14]) : -2],
            table_name=message.content[-1:],
        )
        await message.channel.send(str(response))
    if commands[15] in str(message.content):
        name, item1, item2, item3, item4, item5 = tuple(
            str.split(message.content[len(commands[15]) :], ",")
        )
        response = connector.roll_magic_custom_table(
            discord_channel=message.channel.name,
            user_id=str(message.author.name),
            name=name,
            item_list=[item1, item2, item3, item4, item5],
        )
        await message.channel.send(str(response))
    # if message.content == "Que piensas de Fedor?":
    #    response = "Ufff esta buenorro el tio pero lo tiene pillado ems :("
    #    await message.channel.send(response)


# bot tree commands!:
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
        result = connector.create_character(
            interaction.channel.name,
            str(interaction.user.name),
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

        message = None
        embed = None
        if result is None:
            message = "None"
        elif type(result) == str:
            message = result
        else:
            embed = custom_commands.template_generic(True, result[0], interaction)

        await interaction.response.send_message(message, embed=embed)

    # Declaracion de las funciones de autocompletar
    @nuevo.autocomplete("race")
    async def auto_race(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in connector.get_races(format="race"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    @nuevo.autocomplete("clase")
    async def auto_race(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in connector.get_classes({}, "class"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    # Declaracion de funiones de autocompletar dependientes.
    @nuevo.autocomplete("subrace")
    async def auto_subrace(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        subrace = connector.get_races(
            {"race": interaction.namespace.raza}, format="subrace"
        )
        for races in subrace:
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    @nuevo.autocomplete("subclase")
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
        result = custom_commands.template_personaje(
            connector, interaction.channel.name, name
        )
        message = None
        embed = None
        if type(result) == str:
            message = result
        else:
            embed = result

        await interaction.response.send_message(message, embed=embed)

    # Comando para subir de nivel un personaje.
    @app_commands.command(name="nivel", description="Sube de nivel a un personaje")
    @app_commands.describe(name="Nombre del persasonaje para subir de nivel")
    async def nivel(
        self,
        interaction: discord.Interaction,
        name: str,
        class_name: Optional[str],
        subclass_name: Optional[str],
        life_method_roll: Optional[str],
    ):
        result = connector.level_up(
            interaction.channel.name,
            str(interaction.user.name),
            name,
            class_name,
            subclass_name,
            life_method_roll,
        )  # subir nivel

        message = None
        embed = None
        if result is None:
            message = "None"
        elif type(result) == str:
            message = result
        else:
            embed = custom_commands.template_generic(True, result, interaction)

        await interaction.response.send_message(message, embed=embed)

    # Declaracion de las funciones de autocompletar nombre de pj dependiendo del jugador que interactue
    @nuevo.autocomplete("name")
    async def auto_name(
        self, interaction: discord.Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for races in mongo_connector.mongo_connector.get_races({}, "race"):
            if current.lower() in races.lower():
                data.append(app_commands.Choice(name=races, value=races))
        return data

    # Commando para fijar url de pj
    @app_commands.command(name="imagen", description="Fija la imagen del personaje")
    @app_commands.describe(name="Nombre del personaje", url="Url de la imagen")
    async def imagen(self, interaction: discord.Interaction, name: str, url: str):
        result = connector.set_character_url(
            character=name, player=str(interaction.user.name), url=url
        )  # subir nivel

        await interaction.response.send_message(result)


# bot tree add commands!:
bot.tree.clear_commands(guild=None)
bot.tree.add_command(personaje())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-cli":
            print("starting as client")
            bot.run(TOKEN)

        elif sys.argv[1] == "-bot":
            print("starting as bot")
            bot.run(TOKEN)
    else:
        print("starting as bot: this is the current default behaviour")
        bot.run(TOKEN)
