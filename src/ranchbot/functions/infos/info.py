import discord
from discord import user
from discord import client
from discord.ext import commands

from util.embed import embed


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def info(self, ctx):
        infoEmbed = self.__getInfoEmbed()
        await ctx.send(embed=infoEmbed)

#currently developing avatar embed
    @commands.command()
    async def avatar(self, ctx):
        avatarEmbed = self.__getAvatarEmbed()
        await ctx.send(embed=avatarEmbed)

    @commands.command()
    async def help(self, ctx):
        helpEmbed = self.__getHelpEmbed()
        # function for sending the link of searched term -- kind of like search engine --
        await ctx.send(embed=helpEmbed)

    def __getInfoEmbed(self) -> discord.Embed:
        infoEmbed = embed.getBaseEmbed(discord.Colour.orange())
        infoEmbed.add_field(
            name="Commands", value="Send '$help' for commands.", inline=True
        )
        return infoEmbed

    def __getHelpEmbed(self) -> discord.Embed:
        helpEmbed = embed.getBaseEmbed(discord.Colour.blue())
        helpEmbed.add_field(name="$avatar", value="Shows avatar", inline=False)
        helpEmbed.add_field(name="$info", value="Info about the bot", inline=False)
        helpEmbed.add_field(name="$coinflip", value="Decide your fate", inline=False)
        helpEmbed.add_field(
            name="$mirror", value="Bot mirrors your sentence", inline=False
        )
        helpEmbed.add_field(
            name="$brokethesentence", value="Brokes the sentence", inline=False
        )
        helpEmbed.add_field(name="$guessgame", value="Number guessing game!", inline=False)
        helpEmbed.add_field(
            name="$length", value="Give you length of the sentence", inline=False
        )
        return helpEmbed

    def __getAvatarEmbed(self) -> discord.Embed:
        avatarEmbed = embed.getBaseEmbed(discord.Colour.green())
        avatarEmbed.add_field(name="Avatar viewer", value="This has not been implemented yet...", inline=True)
        return avatarEmbed

def setup(bot):
    bot.add_cog(info(bot))
