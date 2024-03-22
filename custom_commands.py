import discord
from discord.ext import commands
import mongo_connector
import datetime
import os
import validators
from decimal import Decimal


def template_personaje(connector, channel, name: str):
    if channel not in ["bot-test", "consultas"]:
        return "Invalid Channel"
    info = connector.get_character(name)
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
    race = connector.get_race(id=info["Race"])
    race_str = (
        race["race"]
        if "subrace_name" not in race.keys()
        else f"{race['race']}: {race['subrace_name']}"
    )
    template_pj.add_field(name="Raza", value=race_str, inline=True)
    template_pj.add_field(name="HP", value=info["HP"], inline=True)
    template_pj.add_field(
        name="XP",
        value=str(info["XP"])
        + (" / " + str(xp_req) if info["Level"] <= 20 else ""),  # 150/300
        inline=True,
    )

    classes = info["Classes"]
    cl_strs = []
    for cl_key in classes.keys():
        cl = connector.get_class(id=cl_key)
        if "subclass_name" in cl:
            cl_strs.append(f"{cl['class']}, {cl['subclass_name']}: {classes[cl_key]}")
        else:
            cl_strs.append(f"{cl['class']}: {classes[cl_key]}")

    template_pj.add_field(
        name="Clases:",
        value="\n".join(cl_strs),
        inline=False,
    )

    template_pj.add_field(
        name="Feats :",
        value="\n".join(info["Feats"]),
        inline=False,
    )

    template_pj.add_field(
        name="Rewards:",
        value="\n".join(info["Rewards"]),
        inline=False,
    )

    template_pj.add_field(
        name="Money",
        value=str(int(info["GP"]))
        + " gp "
        + str(int(info["GP"] * 10))[-1]
        + " sp "
        + str(int(info["GP"] * 100))[-1]
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


def template_generic(error: bool, respuesta: str, interation: discord.Interaction):
    if error:
        template = discord.Embed(description=respuesta, colour=0xFF0080)

        template.set_author(
            name=interation.user.display_name, icon_url=interation.user.display_icon
        )

    else:
        template = discord.Embed(description=respuesta, colour=0x008080)

        template.set_author(
            name=interation.user.display_name, icon_url=interation.user.display_icon
        )

    return template
