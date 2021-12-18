#!/usr/bin/env python3

import pytest
import discord.ext.test as dpytest
from main import App


@pytest.fixture
def bot(event_loop):
    bot = App("$", "Alive.", event_loop)
    dpytest.configure(bot)
    bot.loadCommands()
    return bot
