import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_connection(self):
        return await r.connect("localhost", 28015)
        
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
                    
    @commands.group(invoke_without_command=True, aliases=['db'])
    async def database(self, ctx):
        pass
        
    @database.command()
    @commands.is_owner()
    async def create(self, ctx, *, database:str):
        conn = await self.get_connection()
        await r.db_create(database).run(conn)
        await ctx.send("Created `{}` successfully!".format(database))
        
    @database.command()
    @commands.is_owner()
    async def delete(self, ctx, *, database:str):
        conn = await self.get_connection()
        await r.db_drop(database).run(conn)
        await ctx.send("Deleted `{}` successfully!".format(database))
        
    @database.command()
    @commands.is_owner()
    async def list(self, ctx):
        conn = await self.get_connection()
        to_iterate = await r.db_list().run(conn)
        text = ""
        for x in to_iterate:
            text += "{}\n".format(x)
            await asyncio.sleep(0)
        await ctx.send(text)
        
def setup(bot):
    bot.add_cog(Owner(bot))