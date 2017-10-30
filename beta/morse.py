import discord
from discord.ext import commands

class Morse:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['m'])
    async def morse(self, ctx):
        pass
        
def setup(bot):
    bot.add_cog(Morse(bot))