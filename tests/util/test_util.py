from hikari import Color
import colour
from ranchbot.util.embed import embed


def test_baseEmbed():
    baseEmbed = embed.getBaseEmbed("Hello World", Color.of(colour.Color("blue").hex))
    assert baseEmbed.title == "Hello World"
    assert baseEmbed.footer.text == "RanchBot"
    assert baseEmbed.author.name == "RanchBot"
