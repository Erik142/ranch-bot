#!/usr/bin/env python3
import colour
import lightbulb

from hikari import Color
from hikari.embeds import Embed

from core.bot import Bot
from util.embed import embed


class Help(lightbulb.Plugin):
    @lightbulb.command("help2", "Prints basic help for all commands")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def help(self, ctx: lightbulb.Context):
        """
        Prints basic help for all commands
        """
        helpEmbed = self.__getHelpEmbed()
        await ctx.respond(embed=helpEmbed)

    def __getHelpEmbed(self) -> Embed:
        helpEmbed = embed.getBaseEmbed("", Color.of(colour.Color("blue").hex))
        helpEmbed.description = "The following commands are available:"


        for command in self.bot.commands:
            helpEmbed.add_field(
                name=self.bot.command_prefix + command.name,
                value=command.help,
                inline=False,
            )

        return helpEmbed


def load(bot: Bot):
    bot.add_plugin(Help(bot))

def unload(bot: Bot):
    bot.remove_plugin("Help")
