from discord.ext import commands
import discord
import datetime

from random import randrange

class Random(commands.Cog):
    """Random utilities."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    async def noppa(self, ctx):
        """Random number."""
        await ctx.send(randrange(100))

def setup(bot):
    bot.add_cog(Random(bot))