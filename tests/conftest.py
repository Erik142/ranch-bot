#!/usr/bin/env python3

import pytest

from core.bot import Bot

@pytest.fixture
def bot(event_loop):
    bot = Bot("$", "Alive.", event_loop)
    return bot
