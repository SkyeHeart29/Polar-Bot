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
        conn = await self.get_connection()
        await r.db("bots").table(str(self.bot.user.id)).update({"playing" : game_name}).run(conn)
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
        
    @database.command(aliases=['tc'])
    @commands.is_owner()
    async def tablecreate(self, ctx, database:str, *, table_name:str):
        conn = await self.get_connection()
        await r.db(database).table_create(table_name).run(conn)
        await ctx.send("Added `{}` to `{}` successfully!".format(table_name, database))
        
    @commands.group(invoke_without_command=True, aliases=['bp'])
    async def botprofile(self, ctx):
        pass
        
    @botprofile.command()
    @commands.is_owner()
    async def create(self, ctx):
        conn = await self.get_connection()
        bot_id = str(self.bot.user.id)
        
        if bot_id in await r.db('bots').table_list().run(conn):
            await ctx.send("Bot profile already exists!")
            return
            
        await r.db("bots").table_create(bot_id).run(conn)
        await r.db("bots").table(bot_id).insert({
            "invite" : "Invite link not set.",
            "error" : "Something's wrong! ```{}```",
            "playing" : "Playing status not set.",
            "ping" : "Hi",
            "server" : "Server link not set.",
        }).run(conn)
        
        await ctx.send("Created bot profile!")
        
    @botprofile.command()
    @commands.is_owner()
    async def invite(self, ctx, *, text:str):
        conn = await self.get_connection()
        await r.db("bots").table(str(self.bot.user.id)).update({"invite" : text}).run(conn)
        await ctx.send("Changed text for `invite` to:\n{}".format(text))

    @botprofile.command()
    @commands.is_owner()
    async def ping(self, ctx, *, text:str):
        conn = await self.get_connection()
        await r.db("bots").table(str(self.bot.user.id)).update({"ping" : text}).run(conn)
        await ctx.send("Changed text for `ping` to:\n{}".format(text))
    
    @botprofile.command()
    @commands.is_owner()
    async def error(self, ctx, *, text:str):
        conn = await self.get_connection()
        await r.db("bots").table(str(self.bot.user.id)).update({"error" : text}).run(conn)
        await ctx.send("Changed the text for errors to:\n{}".format(text))
        
    @botprofile.command()
    @commands.is_owner()
    async def server(self, ctx, *, text:str):
        conn = await self.get_connection()
        await r.db("bots").table(str(self.bot.user.id)).update({"server" : text}).run(conn)
        await ctx.send("Changed text for `server` to:\n{}".format(text))

        
def setup(bot):
    bot.add_cog(Owner(bot))