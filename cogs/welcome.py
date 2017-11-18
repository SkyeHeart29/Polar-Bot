import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Welcome:
    def __init__(self, bot):
        self.bot = bot
    
    async def check_if(self, guild_id, conn):
        if guild_id not in await r.db('welcome').table_list().run(conn):
                await r.db('welcome').table_create(guild_id).run(conn)
                await r.db('welcome').table(guild_id).insert({
                    "toggle": True,
                    "message": "Welcome, {user} to {server}!",
                    "mode": "0",
                    "channel": str(ctx.message.channel.id),
                }).run(conn)
    
    async def get_connection(self):
        return await r.connect("localhost", 28015)
    
    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send("help")
    
    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx):
        conn = await self.get_connection()
        await self.check_if(str(ctx.guild.id), conn)
        
        cursor = await r.db("welcome").table(str(ctx.guild.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item["toggle"] == True:
                await r.db('welcome').table(str(ctx.guild.id)).update({"toggle": False}).run(conn)
                await ctx.send("The welcome message will no longer be sent.")
            elif item["toggle"] == False:
                await r.db('welcome').table(str(ctx.guild.id)).update({"toggle": True}).run(conn)
                await ctx.send("The welcome message will be sent.")
            
    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def message(self, ctx, *, text:str=None):
        conn = await self.get_connection()
        await self.check_if(str(ctx.guild.id), conn)
       
        if text == None:
            await ctx.send("You need to add a message!")
            return
            
        await r.db('welcome').table(str(ctx.guild.id)).update({"message": text}).run(conn)
        await ctx.send("The welcome message has been edited successfully!")
        
    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def mode(self, ctx):
        conn = await self.get_connection()
        await self.check_if(str(ctx.guild.id), conn)
        
        cursor = await r.db("welcome").table(str(ctx.guild.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item["mode"] == "0":
                await r.db('welcome').table(str(ctx.guild.id)).update({"mode": "1"}).run(conn)
                await ctx.send("The welcome message will be sent to the user via DM.")
            elif item["mode"] == "1":
                await r.db('welcome').table(str(ctx.guild.id)).update({"mode": "0"}).run(conn)
                await ctx.send("The welcome message will be sent to <#{}>".format(item["channel"]))
        
    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def here(self, ctx):
        conn = await self.get_connection()
        await self.check_if(str(ctx.guild.id), conn)
        
        channel_id = str(ctx.message.channel.id)
        await r.db('welcome').table(str(ctx.guild.id)).update({"channel": channel_id}).run(conn)
        await ctx.send("The welcome message will be sent to <#{}>".format(channel_id))
            
    async def on_member_join(self, member):        
        conn = await self.get_connection()
        guild_id = str(member.guild.id)
        if guild_id in await r.db('welcome').table_list().run(conn):
            cursor = await r.db("welcome").table(guild_id).run(conn)
            while (await cursor.fetch_next()):
                item = await cursor.next()
                formatting = {
                    'me': member.display_name,
                    'me-username': member.name,
                    'me-user': str(member),
                    'me-discrim': member.discriminator,
                    'me-id': member.id,
                    'channel': self.bot.get_channel(int(item["channel"])).name,
                    'channel-id': item["channel"],
                    'server': member.guild,
                    'server-id': member.guild.id,
                }
                if item["toggle"] == False:
                    return
                if item["mode"] == "0":
                    for channel in member.guild.channels:
                        if str(channel.id) == item["channel"]:
                            await channel.send(content=item["message"].format(**formatting))
                            return
                elif item["mode"] == "1":
                    await member.send(content=item["message"].format(**formatting))
            
def setup(bot):
    bot.add_cog(Welcome(bot))