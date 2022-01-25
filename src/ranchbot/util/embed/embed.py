#!/usr/bin/env python3
from hikari import Color
from hikari.embeds import Embed


def getBaseEmbed(title, colour: Color) -> Embed:
    embed = Embed(title=title, colour=colour)
    embed.set_footer(text="RanchBot")
    embed.set_author(name="RanchBot")
    return embed
