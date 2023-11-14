# bot.py
import os

import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import mongo_connector

entryData = mongo_connector.mongo_connector()


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


@bot.tree.command()
async def personajeinfo(interation: discord.Interaction, name: str):
    if interation.channel_id == 1174044792569724999 :
        persData = entryData.get_character(name)

        if persData:
            persTemp = discord.Embed(
                title=persData["Personaje"],
                description="Del usuario " + persData["Dueño"],
                colour=discord.Color.purple(),
            )

            persTemp.add_field(name="Raza:", value=persData["Race"])
            persTemp.add_field(name="Vida:", value=persData["HP"])
            persTemp.add_field(name="Exp:", value=persData["XP"])
            persTemp.add_field(
                name="Clases",
                value="\n".join(["- " + x for x in (persData["Clases"].split(","))]),
                inline=False,
            )
            persTemp.add_field(name="Fuerza:", value=persData["FUE"])
            persTemp.add_field(name="Destreza:", value=persData["DEX"])
            persTemp.add_field(name="Constitución:", value=persData["CON"])
            persTemp.add_field(name="Inteligencia:", value=persData["INT"])
            persTemp.add_field(name="Sabiduría:", value=persData["WIS"])
            persTemp.add_field(name="Carisma:", value=persData["CHA"])
            persTemp.add_field(
                name="Oro:",
                value=str(int(persData["GP"]))
                + " gp "
                + str(persData["GP"])[-2]
                + " sp "
                + str(persData["GP"])[-1]
                + " cp ",
                inline=False,
            )
            persTemp.add_field(name="Fortuna:", value=persData["Fortuna"])
            persTemp.add_field(name="Prestigio:", value=persData["Prestigio"])
            persTemp.add_field(name="", value="")
            persTemp.add_field(name="Evento:", value=persData["Evento"])
            persTemp.add_field(name="Chikievento:", value=persData["Chikievento"])
            persTemp.add_field(
                name="Rabo", value=persData.get("rabo", "No sabe no responde.")
            )
            persTemp.add_field(name="Descanso:", value=persData["Descanso"])
            persTemp.add_field(
                name="Asi de master:",
                value="Usada" if persData["Stats de master"] else "No Usada",
            )
            persTemp.add_field(
                name="Feat de master:",
                value="Usada" if persData["Feat de Mastter"] else "No Usada",
            )

            await interation.response.send_message(embed=persTemp)

        else:
            await interation.response.send_message("El personaje no existe", ephemeral=True)
    
    else:
        await interation.response.send_message(
            "Canal incorrecto " + interation.user.display_name
        )
        

@bot.tree.command(name="pito")
async def pito(interation: discord.Interaction, name: str):
    if interation.channel_id == 1174044308417028197:
        rabo = entryData.get_character(name).get("rabo")
        if rabo is None :
            entryData.update_character(name)
            await interation.response.send_message("Tu pito es de " + entryData.get_character(name).get("rabo"))
        else : 
            await interation.response.send_message("Te jodes con el pito que tienes.")
    else :
        await interation.response.send_message(
            "Canal incorrecto " + interation.user.display_name
        )


bot.run(TOKEN)
