import discord
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def playing(self, ctx, *, newgame:str):
        await self.bot.change_presence(game=discord.Game(name=newgame))
        
def setup(bot):
    bot.add_cog(Owner(bot))