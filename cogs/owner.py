import discord
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def playing(self, ctx, *, game_name:str):
        await self.bot.change_presence(game=discord.Game(name=game_name))
        
    @commands.command()
    @commands.is_owner()
    async def inform(self, ctx, *, news:str):
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.send(news)
                    break
                except:
                    pass
        
def setup(bot):
    bot.add_cog(Owner(bot))