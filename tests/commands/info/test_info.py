#!/usr/bin/env python3

import asyncio
import pytest

from ranchbot.commands.info.info import Info
import discord.ext.test as dpytest
from discord.embeds import EmbedProxy


def test_infoEmbed():
    info = Info(None)
    infoEmbed = info._Info__getInfoEmbed()

    assert infoEmbed.fields[0].name == "Commands"
    assert infoEmbed.fields[0].value == "Send '$help' for commands."


@pytest.mark.asyncio
async def test_infoCommand(bot):
    info = Info(None)
    await dpytest.message("$info")
    assert dpytest.verify().message().embed(info._Info__getInfoEmbed())
