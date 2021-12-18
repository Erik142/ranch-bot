#!/usr/bin/env python3
import discord


def getBaseEmbed(title, colour: discord.Colour) -> discord.Embed:
    embed = discord.Embed(title=title, colour=colour)
    embed.set_footer(text="RanchBot")
    embed.set_author(name="RanchBot")
    return embed
