#!/usr/bin/env python3
import discord


def getBaseEmbed(colour: discord.Colour) -> discord.Embed:
    embed = discord.Embed(title="RanchBot", colour=colour)
    embed.set_footer(text="RanchBot")
    embed.set_author(name="SeriousCoal|Erkaberkaboi|Stumblingthroughlife|jarrett")
    return embed
