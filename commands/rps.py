from discord.ext import commands
import discord
import datetime

import random

class Rps(commands.Cog):
    """Rock Paper Scissors."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False, aliases=['kps', 'ksp'])
    async def rps(self, ctx, *arg):
        """Erä kps / ksp!"""
        p_arg = []
        for a in arg:
            try:
                a_p = a.strip().lower()
                if a_p in ['kivi', 'rock', 'stone']:
                    p_arg.append('kivi')
                    break
                elif a_p in ['sakset', 'scissors']:
                    p_arg.append('sakset')
                    break
                elif a_p in ['paperi', 'paper']:
                    p_arg.append('paperi')
                    break
            except:
                pass

        if len(p_arg) > 0:
            my_choice = random.choice(['kivi', 'sakset', 'paperi'])

            if my_choice == p_arg[0]:
                await ctx.send('Tasapeli!')
            elif p_arg[0] == 'kivi':
                if my_choice == 'paperi':
                    await ctx.send('Paperi peittää kiven. Voitin!')
                else:
                    await ctx.send('Kivi lyö sakset. Sä voitit!')

            elif p_arg[0] == 'paperi':
                if my_choice == 'sakset':
                    await ctx.send('Sakset leikkaa paperin. Voitin!')
                else:
                    await ctx.send('Paperi peittää kiven. Sä voitit!')

            elif p_arg[0] == 'sakset':
                if my_choice == 'kivi':
                    await ctx.send('Kivi lyö sakset. Voitin!')
                else:
                    await ctx.send('Sakset leikkaa paperin. Sä voitit!')

def setup(bot):
    bot.add_cog(Rps(bot))
