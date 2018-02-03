import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Events:
    def __init__(self, bot):
        self.bot = bot

    async def get_connection(self):
        return await r.connect("localhost", 28015, 'bot')
        
    async def on_ready(self):
        print("Logged in!")
        print("Name: %s" % self.bot.user.name)
        print("ID: %s" % self.bot.user.id)
        print("Discord API version: {}".format(discord.__version__))
        
        conn = await self.get_connection()
        cursor = await r.table('bot').run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            await self.bot.change_presence(game=discord.Game(name=item['playing']))
        await conn.close()
    
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
        else:
            await ctx.send("ERROR:```{}```".format(e))
            
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if channel.id == 292555897820020740:
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await channel.send(item['welcome'].format(member.id))
                await conn.close()
<<<<<<< HEAD
                
    async def on_voice_state_update(self, member, before, after):
        if after.channel == None or after.channel.id == 404965762906849281:
            for erase in member.roles:
                if erase.name == "voice channel 1":
                    await member.remove_roles(erase)
                if erase.name == "voice channel 2":
                    await member.remove_roles(erase)
                    
        elif after.channel.id == 292543650381037568:
            for role in member.guild.roles:
                if role.name == "voice channel 1":
                    await member.add_roles(role)
                    break
            for erase in member.roles:
                if erase.name == "voice channel 2":
                    await member.remove_roles(erase)
                    break
                    
        elif after.channel.id == 336178195302973444:
            for role in member.guild.roles:
                if role.name == "voice channel 2":
                    await member.add_roles(role)
                    break
            for erase in member.roles:
                if erase.name == "voice channel 1":
                    await member.remove_roles(erase)
                    break
=======
>>>>>>> 6044886e47955bc7a4c5fd9c720dbc6cbf45def7
        
def setup(bot):
    bot.add_cog(Events(bot))