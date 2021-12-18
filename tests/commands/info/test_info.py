#!/usr/bin/env python3

import asyncio
import pytest

from commands.infos.info import Info
from main import App
import discord.ext.test as dpytest
from discord.embeds import EmbedProxy


@pytest.fixture
def bot(event_loop):
    bot = App("$", "Alive.", event_loop)
    dpytest.configure(bot)
    bot.loadCommands()
    return bot


def test_infoEmbed():
    info = Info(None)
    infoEmbed = info._Info__getInfoEmbed()

    proxy = EmbedProxy({"name": "Commands", "value": "Send '$help' for commands."})

    assert infoEmbed.fields[0].name == "Commands"
    assert infoEmbed.fields[0].value == "Send '$help' for commands."


@pytest.mark.asyncio
async def test_infoCommand(bot):
    info = Info(None)
    await dpytest.message("$info")
    assert dpytest.verify().message().embed(info._Info__getInfoEmbed())
