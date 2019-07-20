from discord.ext import commands
import discord
import datetime

import random

class Dice(commands.Cog):
    """Dice machine. And some other simple random draws"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    async def tikku(self, ctx, *arg):
        """Draw straws
           Randomly get item from given list. Example:
           ?tikku (a b c d)"""
        carg = ','.join(arg).replace('[', '(').replace(']', ')')
        if '(' in carg:
            carg = carg.split(')')
            items = 1
            try:
                items = int(carg[1].replace(',', ''))
            except:
                pass

            targ = carg[0].translate({ord(c): None for c in '@#$¤()[]{}'}).split(',')
            while '' in targ: targ.remove('')
            while ' ' in targ: targ.remove(' ')
            while ',' in targ: targ.remove(',')
            random.shuffle(targ)

            if len(targ) < 1:
                pass
            elif len(targ) > items:
                await ctx.send("Nostettu {}, jäljellä ({})".format(','.join(targ[:items]), ','.join(targ[items:])))
            else:
                await ctx.send("Nostettu {}, siinä kaikki".format(','.join(targ[:items])))


    @commands.command(hidden=False, aliases=['d', 'r', 'random'])
    async def noppa(self, ctx, *arg):
        """Dice(s) throw.
           Get random number from given range. Example:
           ?random 6 2"""
        #print(f'command: {arg}')
        p_arg = []
        for a in arg:
            try:
                if int(a) > 0: p_arg.append(int(a))
            except:
                pass
        if len(arg) == 0: p_arg.append(6)

        if len(p_arg) == 1:
            await ctx.send(random.randint(1, p_arg[0]))
        elif len(p_arg) == 2:
            nums = []
            for i in range(p_arg[1]):
                nums.append(str(random.randint(1, p_arg[0])))
            await ctx.send(', '.join(nums))

def setup(bot):
    bot.add_cog(Dice(bot))
