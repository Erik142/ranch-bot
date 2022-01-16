#!/usr/bin/env python3

import asyncio
import pytest

from commands.info.info import getInfoEmbed


def test_infoEmbed():
    infoEmbed = getInfoEmbed()

    assert infoEmbed.fields[0].name == "Commands"
    assert infoEmbed.fields[0].value == "Send '$help' for commands."


"""
@pytest.mark.asyncio
async def test_infoCommand(bot):
    info = Info(None)
    await info()
    assert dpytest.verify().message().embed(info._Info__getInfoEmbed())
"""