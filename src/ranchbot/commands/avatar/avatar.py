#!/usr/bin/env python3
import discord
from discord.ext import commands
from util.embed import embed


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def avatar(self, ctx):
        """
        Prints the sender's avatar
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(ctx.author.avatar_url)

    @avatar.command()
    async def user(self, ctx, member: discord.Member):
        """
        Prints the specified user's avatar
        """
        await ctx.send(member.default_avatar_url)


def setup(bot):
    bot.add_cog(Avatar(bot))
