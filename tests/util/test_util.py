import colour
from hikari import Color
from util.embed import embed


def test_baseEmbed():
    baseEmbed = embed.getBaseEmbed("Hello World", Color.of(colour.Color("blue").hex))
    assert baseEmbed.title == "Hello World"
    assert baseEmbed.footer.text == "RanchBot"
    assert baseEmbed.author.name == "RanchBot"
