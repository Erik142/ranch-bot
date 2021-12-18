import discord
from discord.ext import commands

from util.embed import embed


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def info(self, ctx):
        """
        Prints basic command information
        """
        infoEmbed = self.__getInfoEmbed()
        await ctx.send(embed=infoEmbed)

    def __getInfoEmbed(self) -> discord.Embed:
        infoEmbed = embed.getBaseEmbed("info", discord.Colour.orange())
        infoEmbed.add_field(
            name="Commands", value="Send '$help' for commands.", inline=True
        )
        return infoEmbed


def setup(bot):
    bot.add_cog(Info(bot))
