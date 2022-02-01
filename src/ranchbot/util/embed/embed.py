#!/usr/bin/env python3
from hikari import Color
from hikari.embeds import Embed


def getBaseEmbed(title, colour: Color) -> Embed:
    embed = Embed(title=title, colour=colour)
    return embed
