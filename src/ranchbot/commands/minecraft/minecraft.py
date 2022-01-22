#!/usr/bin/env python3

import secrets
import discord
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands

from ranchbot.core.config import Config
from ranchbot.core.database import PostgresDatabase
from ranchbot.util.embed import embed
from ranchbot.util.log import log


class Minecraft(commands.Cog):
    __DATABASE = None
    __LOGGER = None

    def __init__(self, bot):
        self.bot = bot
        self.__LOGGER = log.getLogger(__name__)
        config = Config()
        self.__DATABASE = PostgresDatabase(config.getPostgresConnectionString())

    @slash_command(name="register")
    async def register(self, ctx):
        """
        Registers the user's Discord account for with the Minecraft server
        """
        userId = str(ctx.author.id)

        try:
            if self.__DATABASE.is_player_registered(userId):
                failEmbed = embed.getBaseEmbed("", discord.Colour.red())
                minecraft_user = self.__DATABASE.get_minecraft_user(userId) 
                if minecraft_user == "" or minecraft_user is None:
                    reg_code = self.__DATABASE.get_reg_code(userId)
                    failEmbed.add_field(
                        name="Minecraft registration",
                        value="You have a pending registration status. To complete the registration process, please open Minecraft, connect to The Ranch's Minecraft server, and finally enter the command \n\n```\n/register "
                         + reg_code 
                         + " \n```\n\nto link your Minecraft user to your Discord user.")
                else:
                    failEmbed.add_field(
                        name="Minecraft registration",
                        value="You are already registered on the Minecraft server, please unregister before trying to register again.",
                    )
                await ctx.respond(embed=failEmbed, ephemeral=True)
                return
        except Exception as e:
            self.__LOGGER.error("An error occured while checking the registration status for the user with Discord ID %s: %s", userId, e)
            try:
                errorEmbed = embed.getBaseEmbed("", discord.Colour.red())
                errorEmbed.add_field(
                    name = "Minecraft registration",
                    value="An error occured while checking your registration status. Please try again, and contact one of the moderators if the issue persists."
                )
                await ctx.respond(embed=errorEmbed, ephemeral=True)
            except Exception as e1:
                self.__LOGGER.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)
            return

        reg_code = secrets.token_hex(32)

        try:
            self.__DATABASE.add_player(userId, reg_code)

            registerEmbed = embed.getBaseEmbed("", discord.Colour.blue())
            registerEmbed.add_field(
                name="Minecraft registration",
                value="Finish the registration by opening Minecraft, then connect to The Ranch's Minecraft server. Finally enter the command \n\n```\n/register "
                + reg_code
                + " \n```\n\nto link the Minecraft user to your Discord account.",
            )
            
            await ctx.respond(embed=registerEmbed, ephemeral=True)
        except Exception as e:
            self.__LOGGER.error("An error occured while registering the user with Discord ID %s: %s", userId, e)
            errorEmbed = embed.getBaseEmbed("", discord.Colour.red())
            errorEmbed.add_field(
                name="Minecraft registration",
                value="An error occured while performing the registration. Please try again, and contact one of the moderators if the issue persists."
                )
            try:
                await ctx.respond(embed=errorEmbed, ephemeral=True)
            except Exception as e1:
                self.__LOGGER.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)

    @slash_command(name="unregister")
    async def unregister(self, ctx):
        """
        Unregisters the current Discord user from the Minecraft server, if already registered
        """
        userId = str(ctx.author.id)

        try:
            if self.__DATABASE.is_player_registered(userId) == False:
                failEmbed = embed.getBaseEmbed("", discord.Colour.red())
                failEmbed.add_field(
                    name="Minecraft registration",
                    value="You are not registered on the Minecraft server.",
                )
                await ctx.respond(embed=failEmbed, ephemeral=True)
                return
        except Exception as e:
            self.__LOGGER.error("An error occured while checking the registration status for the user with Discord ID %s: %s", userId, e)
            errorEmbed = embed.getBaseEmbed("", discord.Colour.red())
            errorEmbed.add_field(
                name="Minecraft unregistration",
                value="An error occured while checking the registration status. Please try again, and contact one of the moderators if the issue persists."
            )
            try:
                await ctx.respond(embed=errorEmbed, ephemeral=True)
            except Exception as e1:
                self.__LOGGER.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)
            return            

        try:
            self.__DATABASE.delete_player(userId)

            unregisterEmbed = embed.getBaseEmbed("", discord.Colour.blue())
            unregisterEmbed.add_field(
                name="Minecraft registration",
                value="You have been successfully unregistered from the Minecraft server.",
            )

            await ctx.respond(embed=unregisterEmbed, ephemeral=True)
        except Exception as e:
            self.__LOGGER.error("An error occured while unregistering the user with Discord ID %s: %s", userId, e)
            errorEmbed = embed.getBaseEmbed("", discord.Colour.red())
            errorEmbed.add_field(
                name="Minecraft unregistration",
                value="An error occured while unregistering. Please try again, and contact one of the moderators if the issue persists."
            )
            try:
                await ctx.respond(embed=errorEmbed, ephemeral=True)
            except Exception as e1:
                self.__LOGGER.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)


def setup(bot):
    bot.add_cog(Minecraft(bot))
