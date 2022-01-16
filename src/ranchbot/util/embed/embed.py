#!/usr/bin/env python3
from hikari import Color
from hikari.embeds import Embed, EmbedAuthor, EmbedFooter

def getBaseEmbed(title, colour: Color) -> Embed:
    embed = Embed(title=title, colour=colour)
    embed.footer = EmbedFooter(text="RanchBot")
    embed.author = EmbedAuthor(name="RanchBot")
    return embed
