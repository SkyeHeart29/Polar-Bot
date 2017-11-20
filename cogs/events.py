import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Events:
    def __init__(self, bot):
        self.bot = bot

    async def get_connection(self):
        return await r.connect("localhost", 28015)
        
    async def on_ready(self):
        print("Logged in!")
        print("Name: %s" % self.bot.user.name)
        print("ID: %s" % self.bot.user.id)
        print("Discord API version: {}".format(discord.__version__))
        
        conn = await self.get_connection()
        cursor = await r.db("bots").table(str(self.bot.user.id)).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            await self.bot.change_presence(game=discord.Game(name=item["playing"]))
    
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        elif message.content == "<@{}>".format(self.bot.user.id):
            try:
                conn = await self.get_connection()
                guild_id = str(message.guild.id)
                cursor = await r.db("bots").table(str(self.bot.user.id)).run(conn)
                cursor2 = await r.db("properties").table(str(self.bot.user.id)+guild_id).run(conn)
                text = ""
            
                while (await cursor2.fetch_next()):
                    item = await cursor2.next()
                    text += "Prefix: {}\n".format(item["prefix"])
            
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    text += item["ping"]
                
                await message.channel.send(text)
                
            except:
                pass
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
        else:
            conn = await self.get_connection()
            cursor = await r.db("bots").table(str(self.bot.user.id)).run(conn)
            while (await cursor.fetch_next()):
                item = await cursor.next()
                await ctx.send(item["error"].format(e))

        
def setup(bot):
    bot.add_cog(Events(bot))