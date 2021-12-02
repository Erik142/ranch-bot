import discord
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def info(self, ctx):
        info_board = discord.Embed(
            title="NakedCowboy",
            description="Naked Cowboy for The Ranch server",
            colour=discord.Colour.orange()
        )
        info_board.set_footer(text="NakedCowboy")
        info_board.set_author(name="By SeriousCoal")
        info_board.add_field(name="Commands", value="Send '$help' for commands.", inline=True)
        await ctx.send(embed=info_board)

    @commands.command()
    async def avatar(self, ctx):
        await ctx.send(ctx.author.avatar_url)

    @commands.command()
    async def help(self, ctx):
        info_board = discord.Embed(
            title="NakedCowboy",
            colour=discord.Colour.blue()
        )
        info_board.set_footer(text="NakedCowboy")
        info_board.set_author(name="SeriousCoal")
        info_board.add_field(name="$avatar", value="Shows avatar.", inline=False)
        info_board.add_field(name="$info", value="Info about the bot.", inline=False)
        info_board.add_field(name="$coinflip", value="Decide your fate.", inline=False)
        info_board.add_field(name="$mirror", value="Bot mirrors your sentence.", inline=False)
        info_board.add_field(name="$brokethesentence", value='Brokes the sentence.', inline=False)
        info_board.add_field(name="$length", value='Give you length the sentence.', inline=False)
        #function for sending the link of searched term -- kind of like search engine --
        await ctx.send(embed=info_board)


def setup(bot):
    bot.add_cog(info(bot))