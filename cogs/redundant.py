import asyncio
import discord
from discord.ext import commands

class Redundant:
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command()
    async def summon(self, ctx):
        pass
        
    @commands.command()
    async def play(self, ctx):
        pass
        
    @commands.command()
    async def volume(self, ctx):
        pass
        
    @commands.command()
    async def pause(self, ctx):
        pass
        
    @commands.command()
    async def resume(self, ctx):
        pass
    
    @commands.command()
    async def stop(self, ctx):
        pass
        
    @commands.command()
    async def skip(self, ctx):
        pass
        
    @commands.command()
    async def forceskip(self, ctx):
        pass
        
    @commands.command()
    async def playlist(self, ctx):
        pass
        
def setup(bot):
    bot.add_cog(Redundant(bot))