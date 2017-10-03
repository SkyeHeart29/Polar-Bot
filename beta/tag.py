import asyncio
import discord
import rethinkdb as r
from twisted.internet import reactor, defer
from twisted.internet.defer import inlineCallbacks, returnValue
from discord.ext import commands

class Tag:
    def __init__(self, bot):
        self.bot = bot
    
    @inlineCallbacks
    @commands.group(aliases=['t'])
    @commands.has_permissions(ban_members=True)
    async def tag(self, ctx, tag_name):
        r
        
    @inlineCallbacks    
    async def create(self, ctx, tag_name, *, content:str=None):
        if content == None:
            ctx.send("You need to add some content!")
            return
        else:
            conn = await conn_deferred
            guild_id = str(ctx.guild.id)
            if guild_id not in await r.db('tags').tableList().run(conn):
                await r.db('tags').table_create(guild_id).run(conn)
            
def setup(bot):
    r.set_loop_type('twisted')
    connection = r.connect(host='localhost', port=28015)
    bot.add_cog(Tag(bot))