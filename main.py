import discord
from discord.ext import commands

import env

intents = discord.Intents.default()

#only 'info' functions for starting point
cogs: list = ["Functions.infos.info"]

client = commands.Bot(command_prefix=env.Prefix, help_command=None, intents=intents)


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(env.Status))
    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            client.load_extension(cog)
            print(f"Loaded cog {cog}")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))



client.run(env.TOKEN)