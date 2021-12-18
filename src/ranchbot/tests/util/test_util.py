import discord
from ranchbot.util.embed import embed

def test_baseEmbed():
    baseEmbed = embed.getBaseEmbed(discord.Colour.blue())
    assert baseEmbed.title == "RanchBot"
    assert baseEmbed.footer.text == "RanchBot"
    assert baseEmbed.author.name == "SeriousCoal|Erkaberkaboi|Stumblingthroughlife|jarrett"