import discord
from util.embed import embed


def test_baseEmbed():
    baseEmbed = embed.getBaseEmbed("Hello World", discord.Colour.blue())
    assert baseEmbed.title == "Hello World"
    assert baseEmbed.footer.text == "RanchBot"
    assert baseEmbed.author.name == "RanchBot"
