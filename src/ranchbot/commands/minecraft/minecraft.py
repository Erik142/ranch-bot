#!/usr/bin/env python3

from hikari import Color
from hikari.messages import MessageFlag
import lightbulb
import colour

import secrets
from ranchbot.core.bot import Bot

from ranchbot.core.config import Config
from ranchbot.core.database import PostgresDatabase
from ranchbot.util.embed import embed
from ranchbot.util.log import log

minecraft_plugin = lightbulb.Plugin("Minecraft")

database = None
logger = None

bot = None
logger = log.getLogger(__name__)
config = Config()
database = PostgresDatabase(config.getPostgresConnectionString())

@minecraft_plugin.command
@lightbulb.command("minecraft", "Minecraft commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def minecraft(ctx: lightbulb.Context) -> None:
    pass

@minecraft.child
@lightbulb.command("register", "Registers the user's Discord account with the Minecraft server")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def register(ctx: lightbulb.Context) -> None:
    """
    Registers the user's Discord account for with the Minecraft server
    """
    userId = str(ctx.author.id)

    try:
        if database.is_player_registered(userId):
            failEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
            minecraft_user = database.get_minecraft_user(userId) 
            if minecraft_user == "" or minecraft_user is None:
                reg_code = database.get_reg_code(userId)
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
            await ctx.respond(embed=failEmbed, flags=MessageFlag.EPHEMERAL)
            return
    except Exception as e:
        logger.error("An error occured while checking the registration status for the user with Discord ID %s: %s", userId, e)
        try:
            errorEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
            errorEmbed.add_field(
                name = "Minecraft registration",
                value="An error occured while checking your registration status. Please try again, and contact one of the moderators if the issue persists."
            )
            await ctx.respond(embed=errorEmbed, flags=MessageFlag.EPHEMERAL)
        except Exception as e1:
            logger.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)
        return

    reg_code = secrets.token_hex(32)

    try:
        database.add_player(userId, reg_code)

        registerEmbed = embed.getBaseEmbed("", Color.of(colour.Color("blue").hex))
        registerEmbed.add_field(
            name="Minecraft registration",
            value="Finish the registration by opening Minecraft, then connect to The Ranch's Minecraft server. Finally enter the command \n\n```\n/register "
            + reg_code
            + " \n```\n\nto link the Minecraft user to your Discord account.",
        )
        
        await ctx.respond(embed=registerEmbed, flags=MessageFlag.EPHEMERAL)
    except Exception as e:
        logger.error("An error occured while registering the user with Discord ID %s: %s", userId, e)
        errorEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
        errorEmbed.add_field(
            name="Minecraft registration",
            value="An error occured while performing the registration. Please try again, and contact one of the moderators if the issue persists."
            )
        try:
            await ctx.respond(embed=errorEmbed, flags=MessageFlag.EPHEMERAL)
        except Exception as e1:
            logger.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)

@minecraft.child
@lightbulb.command("unregister", "Unregisters the user's Discord account from the Minecraft server")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unregister(ctx: lightbulb.Context) -> None:
    """
    Unregisters the current Discord user from the Minecraft server, if already registered
    """
    userId = str(ctx.author.id)

    try:
        if database.is_player_registered(userId) == False:
            failEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
            failEmbed.add_field(
                name="Minecraft registration",
                value="You are not registered on the Minecraft server.",
            )
            await ctx.respond(embed=failEmbed, flags=MessageFlag.EPHEMERAL)
            return
    except Exception as e:
        logger.error("An error occured while checking the registration status for the user with Discord ID %s: %s", userId, e)
        errorEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
        errorEmbed.add_field(
            name="Minecraft unregistration",
            value="An error occured while checking the registration status. Please try again, and contact one of the moderators if the issue persists."
        )
        try:
            await ctx.respond(embed=errorEmbed, flags=MessageFlag.EPHEMERAL)
        except Exception as e1:
            logger.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)
        return            

    try:
        database.delete_player(userId)

        unregisterEmbed = embed.getBaseEmbed("", Color.of(colour.Color("blue").hex))
        unregisterEmbed.add_field(
            name="Minecraft registration",
            value="You have been successfully unregistered from the Minecraft server.",
        )

        await ctx.respond(embed=unregisterEmbed, flags=MessageFlag.EPHEMERAL)
    except Exception as e:
        logger.error("An error occured while unregistering the user with Discord ID %s: %s", userId, e)
        errorEmbed = embed.getBaseEmbed("", Color.of(colour.Color("red").hex))
        errorEmbed.add_field(
            name="Minecraft unregistration",
            value="An error occured while unregistering. Please try again, and contact one of the moderators if the issue persists."
        )
        try:
            await ctx.respond(embed=errorEmbed, flags=MessageFlag.EPHEMERAL)
        except Exception as e1:
            logger.error("An error occured while sending an error message to the user with Discord ID %s: %s", userId, e1)


def load(bot: Bot):
    bot.add_plugin(minecraft_plugin)

def unload(bot: Bot):
    bot.remove_plugin("Minecraft")