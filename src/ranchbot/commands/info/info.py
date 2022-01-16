import colour
from hikari import Color
from hikari.embeds import Embed
import lightbulb

from util.embed import embed
from core.bot import Bot


class Info(lightbulb.Plugin):
    @lightbulb.command("info", "Prints basic command information")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def info(self, ctx):
        """
        Prints basic command information
        """
        infoEmbed = self.__getInfoEmbed()
        await ctx.send(embed=infoEmbed)

    def __getInfoEmbed(self) -> Embed:
        infoEmbed = embed.getBaseEmbed("info", Color(colour.Color("orange").hex))
        infoEmbed.add_field(
            name="Commands", value="Send '$help' for commands.", inline=True
        )
        return infoEmbed


def load(bot: Bot) -> None:
    bot.add_plugin(Info(bot))

def unload(bot: Bot) -> None:
    bot.remove_plugin("Info")
