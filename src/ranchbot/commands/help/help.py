#!/usr/bin/env python3
import discord
from discord.ext import commands
from util.embed import embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """
        Prints basic help for all commands
        """
        helpEmbed = self.__getHelpEmbed()
        await ctx.send(embed=helpEmbed)

    def __getHelpEmbed(self) -> discord.Embed:
        helpEmbed = embed.getBaseEmbed("", discord.Colour.blue())
        helpEmbed.description = "The following commands are available:"

        for command in self.bot.commands:
            helpEmbed.add_field(
                name=self.bot.command_prefix + command.name,
                value=command.help,
                inline=False,
            )

        return helpEmbed


def setup(bot):
    bot.add_cog(Help(bot))
