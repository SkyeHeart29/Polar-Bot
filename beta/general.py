import discord
import rethinkdb as r
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot
        
    async def get_connection(self):
        return await r.connect("localhost", 28015)

    @commands.command()
    async def connections(self, ctx):
        await ctx.send("I'm in {} servers.".format(len(self.bot.guilds)))

    @commands.command()
    async def invite(self, ctx):
        conn = await self.get_connection()
        cursor = await r.db("bots").table(str(self.bot.user.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            await ctx.send(item["invite"])

    @commands.group(invoke_without_command=True)
    async def help(self, ctx, snippet:str=None):
        conn = await self.get_connection()
        cursor = await r.db("help").table(str(self.bot.user.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if snippet == None and item["name"] == "0":
                await ctx.send(item["content"])
                return
            elif snippet == item["name"]:
                await ctx.send(item["content"])
                return
        await ctx.send("Help page not found.")

    @help.command()
    @commands.is_owner()
    async def create(self, ctx, name:str, *, content:str=None):
        conn = await self.get_connection()
        if str(self.bot.user.id) not in await r.db('help').table_list().run(conn):
            await r.db('help').table_create(str(self.bot.user.id)).run(conn)
        if content == None:
            await ctx.send("You need to add some content!")
            return
            
        await r.db("help").table(str(self.bot.user.id)).insert({
            "name" : name,
            "content" : content,
        }).run(conn)
        await ctx.send("Created `{}` help page successfully!".format(name))
        
    @help.command()
    @commands.is_owner()
    async def update(self, ctx, name:str, *, content:str=None):
        conn = await self.get_connection()
        if content == None:
            await ctx.send("You need to add some content!")
            return
            
        await r.db("help").table(str(self.bot.user.id)).filter({"name" : name}).update({"content" : content}).run(conn)
        await ctx.send("Updated `{}` help page successfully!".format(name))
        
    @help.command()
    @commands.is_owner()
    async def remove(self, ctx, name):
        conn = await self.get_connection()
        await r.db("help").table(str(self.bot.user.id)).filter(r.row["name"] == name).delete().run(conn)
        await ctx.send("Removed `{}` help page successfully!".format(name))
        
    @help.command()
    @commands.is_owner()
    async def list(self, ctx):
        conn = await self.get_connection()
        cursor = await r.db("help").table(str(self.bot.user.id)).run(conn)
        text = ""
        while (await cursor.fetch_next()):
            item = await cursor.next()
            text += "`{}`, ".format(item["name"])
        to_send = text[:-2]
        await ctx.send(to_send)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, new_prefix:str):
        conn = await self.get_connection()
        guild_id = str(ctx.guild.id)
        
        if "`" in new_prefix:
            await ctx.send('Sorry, you cannot have the character ` or in your prefix.')
            return
        
        if str(self.bot.user.id)+guild_id not in await r.db('properties').table_list().run(conn):
            await r.db('properties').table_create(str(self.bot.user.id)+guild_id).run(conn)
            await r.db('properties').table(str(self.bot.user.id)+guild_id).insert({
                "prefix": ".",
            }).run(conn)
        
        await r.db('properties').table(str(self.bot.user.id)+guild_id).update({"prefix": new_prefix}).run(conn)
        await ctx.send("New prefix: {}".format(new_prefix))
    
    @commands.command()
    async def server(self, ctx):
        conn = await self.get_connection()
        cursor = await r.db("bots").table(str(self.bot.user.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            await ctx.send(item["server"])
        
def setup(bot):
    bot.add_cog(General(bot))