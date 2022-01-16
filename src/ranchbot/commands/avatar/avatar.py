#!/usr/bin/env python3
import hikari
import lightbulb

from core.bot import Bot
from util.embed import embed


avatar_plugin = lightbulb.Plugin("Avatar")

@avatar_plugin.command
@lightbulb.command("avatar", "Prints the sender's avatar")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def avatar(ctx: lightbulb.Context) -> None:
    """
    Prints the sender's avatar
    """
    await ctx.respond(ctx.author.avatar_url)

@avatar_plugin.command
@avatar.child
@lightbulb.option("user", "Print this user's avatar", type=hikari.User)
@lightbulb.command("user", "Prints the specified user's avatar")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def user(ctx: lightbulb.Context) -> None:
    """
    Prints the specified user's avatar
    """
    member = ctx.options.user
    await ctx.respond(member.default_avatar_url)


def load(bot: Bot):
    bot.add_plugin(avatar_plugin)

def unload(bot: Bot):
    bot.remove_plugin("Avatar")