#!/usr/bin/env python3

import pytest
import discord.ext.test as dpytest
from core.bot import Bot


@pytest.fixture
def bot(event_loop):
    bot = Bot("$", "Alive.", event_loop)
    dpytest.configure(bot)
    bot.loadCommands()
    return bot
