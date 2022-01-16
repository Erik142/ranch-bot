#!/usr/bin/env python3
import colour
import lightbulb

from hikari import Color
from hikari.embeds import Embed

from core.bot import Bot
from util.embed import embed

class CustomHelp(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context):
        # Override this method to change the message sent when the help command
        # is run without any arguments.
        self.bot.user_commands

    async def send_plugin_help(self, context: lightbulb.Context, plugin: str):
        # Override this method to change the message sent when the help command
        # argument is the name of a plugin.
        ...

    async def send_command_help(self, context: lightbulb.Context, command: str):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command.
        ...

    async def send_group_help(self, context: lightbulb.Context, group: str):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command group.
        ...

    async def object_not_found(self, context: lightbulb.Context, obj: str):
        # Override this method to change the message sent when help is
        # requested for an object that does not exist
        ...


def load(bot: Bot):
    """
    TODO: Load this help command instead of the standard one
    """
#    bot.add_plugin(Help(bot))
    pass

def unload(bot: Bot):
#    bot.remove_plugin("Help")
    pass
