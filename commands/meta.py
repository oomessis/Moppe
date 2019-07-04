from discord.ext import commands
import discord
import datetime

class Meta(commands.Cog):
    """Bot command utilities."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def hello(self, ctx):
        """Displays my intro message."""
        await ctx.send('Hei!')

def setup(bot):
    bot.add_cog(Meta(bot))