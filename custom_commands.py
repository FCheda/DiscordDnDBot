import discord
from discord.ext import commands
import mongo_connector
import datetime
import os
import validators


def template_personaje(entryData, message, name: str):
    info = entryData.get_character(name)
    if info is None:
        return f"No se ha encontrado ningun personaje con el nombre {name}"

    xps = [
        300,
        900,
        2700,
        6500,
        14000,
        23000,
        34000,
        48000,
        64000,
        85000,
        100000,
        120000,
        140000,
        165000,
        195000,
        225000,
        265000,
        305000,
        355000,
    ]
    xp_req = xps[info["Level"] - 1] if info["Level"] <= 20 else 0
    # Indicado para revisar por el tema de guardar el lvl

    template_pj = discord.Embed(
        title=info["Personaje"] + " LvL " + str(info["Level"]),
        colour=0x800080,
        timestamp=datetime.datetime.now(),
    )  # Indicado para revisar por el tema de guardar el lvl.
    """
    template_pj.set_author(
        name=interation.guild.get_member(info["Dueño"]).display_name, icon_url=interation.guild.get_member(info["Dueño"]).display_avatar
    )"""

    template_pj.add_field(name="Fuerza:", value=info["FUE"], inline=True)
    template_pj.add_field(name="Destreza:", value=info["DEX"], inline=True)
    template_pj.add_field(name="Constitución:", value=info["CON"], inline=True)
    template_pj.add_field(name="Inteligencia:", value=info["INT"], inline=True)
    template_pj.add_field(name="Sabiduría:", value=info["WIS"], inline=True)
    template_pj.add_field(name="Carisma:", value=info["CHA"], inline=True)
    template_pj.add_field(name="Raza", value=info["Race"], inline=True)
    template_pj.add_field(name="HP", value=info["HP"], inline=True)
    template_pj.add_field(
        name="XP",
        value=str(info["XP"])
        + (" / " + str(xp_req) if info["Level"] <= 20 else ""),  # 150/300
        inline=True,
    )
    template_pj.add_field(
        name="Clases:",
        value="\n".join(["- " + x for x in (info["Clases"].split(","))]),
        inline=False,
    )
    template_pj.add_field(
        name="Money",
        value=str(int(info["GP"]))
        + " gp "
        + str(info["GP"])[-2]
        + " sp "
        + str(info["GP"])[-1]
        + " cp ",
        inline=False,
    )
    template_pj.add_field(name="Dias Descanso:", value=info["Descanso"], inline=True)
    template_pj.add_field(name="P. Fortuna:", value=info["Fortuna"], inline=True)
    template_pj.add_field(name="P. Prestigio:", value=info["Prestigio"], inline=True)
    template_pj.add_field(name="Minievento:", value=info["Chikievento"], inline=True)
    template_pj.add_field(name="Evento:", value=info["Evento"], inline=True)

    # Saber si guarda un archivo de imagen o una URL, preferentemente URL, Accesible para discord.
    url = info.get("image_url", None)
    if url is not None and validators.url(url):
        template_pj.set_image(url=url)  # invalid url
    elif url is not None:
        print("!!!!! url badly formed")

    """
    template_pj.set_footer(
        text=interation.user.display_name, icon_url=interation.user.display_avatar
    )"""

    return template_pj
