#!/usr/bin/env python3

import discord
from discord.ext import commands

from core.config import Config
from core.database import PostgresDatabase
from util.embed import embed
from util.log import log


class Minecraft(commands.Cog):
    __DATABASE = None
    __LOGGER = None

    def __init__(self, bot):
        self.bot = bot
        self.__LOGGER = log.getLogger(__name__)
        config = Config()
        self.__DATABASE = PostgresDatabase(config.getPostgresConnectionString())

    @commands.group()
    async def minecraft(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @minecraft.command()
    async def register(self, ctx, minecraftUser: str):
        """
        Registers the specified Minecraft user in the Minecraft server and maps it to the user's Discord account
        """
        userId = str(ctx.author.id)

        if self.__DATABASE.isPlayerRegistered(userId):
            failEmbed = embed.getBaseEmbed("", discord.Colour.red())
            failEmbed.add_field(
                name="Minecraft registration",
                value="You are already registered on the Minecraft server, please unregister before trying to register again.",
            )
            await ctx.send(embed=failEmbed)
            return

        self.__DATABASE.addPlayer(userId, minecraftUser)

        registerEmbed = embed.getBaseEmbed("", discord.Colour.blue())
        registerEmbed.add_field(
            name="Minecraft registration",
            value="The user "
            + minecraftUser
            + " has been successfully registered to your Discord account.",
        )

        await ctx.send(embed=registerEmbed)

    @minecraft.command()
    async def unregister(self, ctx):
        """
        Unregisters the current Discord user from the Minecraft server, if already registered
        """
        userId = str(ctx.author.id)

        if self.__DATABASE.isPlayerRegistered(userId) == False:
            failEmbed = embed.getBaseEmbed("", discord.Colour.red())
            failEmbed.add_field(
                name="Minecraft registration",
                value="You are not registered on the Minecraft server.",
            )
            await ctx.send(embed=failEmbed)
            return

        minecraftUser = self.__DATABASE.getMinecraftUser(userId)
        self.__DATABASE.deletePlayer(userId)

        unregisterEmbed = embed.getBaseEmbed("", discord.Colour.blue())
        unregisterEmbed.add_field(
            name="Minecraft registration",
            value="The user "
            + minecraftUser
            + " has been successfully unregistered from your Discord account.",
        )

        await ctx.send(embed=unregisterEmbed)


def setup(bot):
    bot.add_cog(Minecraft(bot))
