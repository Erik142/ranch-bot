from ast import alias
import colour
from hikari import Color
from hikari.embeds import Embed
import lightbulb

from util.embed import embed
from core.bot import Bot

info_plugin = lightbulb.Plugin("Info")

@info_plugin.command
@lightbulb.command(name="info", description="Prints basic command information", aliases=["i, info"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def info(ctx):
    """
    Prints basic command information
    """
    infoEmbed = getInfoEmbed()
    await ctx.respond(embed=infoEmbed)

def getInfoEmbed() -> Embed:
    infoEmbed = embed.getBaseEmbed("info", Color.of(colour.Color("orange").hex))
    infoEmbed.add_field(
        name="Commands", value="Send '$help' for commands.", inline=True
    )
    return infoEmbed


def load(bot: Bot) -> None:
    bot.add_plugin(info_plugin)

def unload(bot: Bot) -> None:
    bot.remove_plugin("Info")
