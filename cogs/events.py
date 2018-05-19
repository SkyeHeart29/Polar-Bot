import asyncio
import discord
import rethinkdb as r
from discord.ext import commands


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.muted_asshats = open('./data/muted.txt').read().split()


    async def postfile(self, filename):
        with open('./data/{}.txt'.format(filename)) as file:
            return file.read()
        
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member:discord.Member=None):
        if member == None:
            await ctx.send('Usage: `+mute (member)`')
            return
        
        id = str(member.id)
        members = open('./data/muted.txt').read().split()
        
        if id in members:
            members.remove(id)
            with open('./data/muted.txt', 'w') as file:
                for x in members:
                    file.write(x + '\n')
            await ctx.send('Unmuted {}.'.format(str(member)))
            
        elif id not in members:
            with open('./data/muted.txt', 'a') as file:
                file.write(id + '\n')
            await ctx.send('Muted {}.'.format(str(member)))
            
        self.muted_asshats = open('./data/muted.txt').read().split()
                
        
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
        
        if str(message.author.id) in self.muted_asshats:
            await message.delete()
    
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
            
        else:
            await ctx.send("ERROR:```{}```".format(e))
            
            
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if channel.id == 292555897820020740:
                text = await self.postfile('welcome')
                await channel.send(text.format(member.id, member.name.upper(), member.name.upper()))
                
                
    async def on_voice_state_update(self, member, before, after):
        ids = [
            (   # voice channel ID
            292543650381037568,
            434380571871936512,
            336178195302973444,
            ),
            
            (   # role ID
            404964203779194890,
            404964396150947840,
            434576504031150090,
            )   
        ]
        
        if after.channel == None or after.channel.id == 404965762906849281: # AFK Channel ID
            for role in member.roles:
                if role.id in ids[1]:
                    await member.remove_roles(role)
                    break
                    
        elif after.channel.id in ids[0]:
            num = ids[0].index(after.channel.id)
            
            # remove voice roles
            for role in member.roles:
                if role.id in ids[1]:
                    await member.remove_roles(role)
                    break
                    
            # add voice roles
            for role in member.guild.roles:
                if role.id == ids[1][num]:
                    await member.add_roles(role)
                    break
        
        
def setup(bot):
    bot.add_cog(Events(bot))