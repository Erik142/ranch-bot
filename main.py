import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")
status = os.environ.get("STATUS")
prefix = os.environ.get("PREFIX")

if token is None:
    print(
        "The token could not be retrieved from environment variables. Please set the TOKEN environment variable and try again."
    )

if status is None:
    print(
        "The activity status could not be retrieved from environment variables. Please set the STATUS environment variable and try again."
    )

if prefix is None:
    print(
        "The command prefix could not be retrieved from environment variables. Please set the PREFIX environment variable and try again."
    )


intents = discord.Intents.default()

# only 'info' functions for starting point
cogs: list = ["Functions.infos.info"]

client = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game(status)
    )
    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            client.load_extension(cog)
            print(f"Loaded cog {cog}")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))


client.run(token)
