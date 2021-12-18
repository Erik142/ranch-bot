#!/usr/bin/env python3

import asyncio
import pytest

from commands.help.help import Help
import discord.ext.test as dpytest
from discord.embeds import EmbedProxy


@pytest.mark.asyncio
def test_helpEmbed(bot):
    help = Help(bot)
    helpEmbed = help._Help__getHelpEmbed()

    i = 0

    for command in bot.commands:
        assert helpEmbed.fields[i].name == bot.command_prefix + command.name
        assert helpEmbed.fields[i].value == command.help
        assert helpEmbed.fields[i].inline == False
        i += 1


@pytest.mark.asyncio
async def test_helpCommand(bot):
    help = Help(bot)
    await dpytest.empty_queue()
    await dpytest.message("$help")
    helpEmbed = help._Help__getHelpEmbed()
    botEmbed = dpytest.get_embed()

    i = 0

    for field in helpEmbed.fields:
        assert field.name == botEmbed.fields[i].name
        assert field.value == botEmbed.fields[i].value
        assert field.inline == botEmbed.fields[i].inline
        i += 1
