import discord
import rethinkdb as r
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_connection(self):
        return await r.connect("localhost", 28015, 'bot')
        
    @commands.command()
    @commands.is_owner()
    async def playing(self, ctx, playing:str):
        conn = await self.get_connection()
        await r.table('bot').update({'playing': playing}).run(conn)
        await conn.close()
        await self.bot.change_presence(game=discord.Game(name=playing))
        await ctx.send("The playing status has been changed.")
        
    @commands.command()
    @commands.is_owner()
    async def welcome(self, ctx, welcome:str):
        conn = await self.get_connection()
        await r.table('bot').update({'welcome': welcome}).run(conn)
        await conn.close()
        await ctx.send("The welcome message has been changed.")
        
    @commands.command()
    @commands.is_owner()
    async def rm(self, ctx, no:str, text:str):
        conn = await self.get_connection()
        await r.table('bot').update({'rm{}'.format(no): text}).run(conn)
        await conn.close()
        await ctx.send("Role Message {} has been changed.".format(no))
        
def setup(bot):
    bot.add_cog(Owner(bot))