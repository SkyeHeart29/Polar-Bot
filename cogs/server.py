import cogs._abstr as abstr
import aiohttp
import asyncio
import bs4
import discord
import datetime
import pytz
import re
from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot
        
        
    async def get_connection(self):
        return await r.connect("localhost", 28015)

        
    async def convert_datetime(self, tbc):
        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Asia/Kuala_Lumpur")
        present = old_timezone.localize(tbc).astimezone(new_timezone)
        text = present.strftime('%A %Y-%m-%d %H:%M:%S (UTC+8)')
        return text
     
     
    @commands.command()
    async def help(self, ctx, arg='help'):
        slate = discord.Embed(colour=7506394)
        terms = {
            'help' : 'help_en',
            'tag' : 'tag_en',
        }
        
        if arg in terms:
            with open('./data/{}.txt'.format(terms[arg])) as file:
                text = file.read()
                slate.description = text
            await ctx.send(embed=slate)
            
        else:
            await ctx.send('Help page not found.')
            
       
    @commands.command()  
    async def panduan(self, ctx, arg='panduan'):
        slate = discord.Embed(colour=7506394)
        terms = {
            'panduan' : 'help_ms',
            'penanda' : 'tag_ms',
        }
        
        if arg in terms:
            with open('./data/{}.txt'.format(terms[arg])) as file:
                text = file.read()
                slate.description = text
            await ctx.send(embed=slate)
            
        else:
            await ctx.send('Halaman panduan tidak dijumpai.')

        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
        
        
    @commands.command()
    async def info(self, ctx, person:discord.Member=None):
        if person == None:
            person = ctx.author
        slate = discord.Embed(title='{} (Displayed as {})'.format(str(person), person.display_name), colour=7506394)
        
        if person.game == None:
            game = 'Nothing'
        
        else:
            game = person.game.name
            
        roles = ''
        for y in [x.name for x in person.roles][1:]:
            roles += y + '\n'
      
        if person.voice == None:
            voice = 'Not Connected'
            
        else:
            voice = 'Connected to {}'.format(person.voice.channel.name)
        
        discord_join_date = await self.convert_datetime(person.created_at)
        server_join_date = await self.convert_datetime(person.joined_at)
        
        fields = [
            ('STATUS', str(person.status), True),
            ('PLAYING', game, True),
            ('VOICE STATUS', voice, True),
            ('AVATAR URL', '[Link]({})'.format(person.avatar_url), True),
            ('DISCORD JOIN DATE', discord_join_date, False),
            ('SERVER JOIN DATE', server_join_date, False),
            ('ROLES', roles, False),
        ]
        
        for x in fields:
            slate.add_field(name=x[0], value=x[1], inline=x[2])
        
        slate.set_thumbnail(url=person.avatar_url)
        slate.set_footer(text='USERNAME ID: {}'.format(person.id))
            
        await ctx.send(embed=slate)

        
    @commands.command()
    async def server(self, ctx):
        guild = ctx.guild
        emoji_text = '**EMOJI**\n' + ''.join([str(emoji) for emoji in guild.emojis])
        slate = discord.Embed(title=guild.name, description=emoji_text, colour=7506394)
        
        creation_date = await self.convert_datetime(guild.created_at)
        afk_text = str(int(guild.afk_timeout / 60)) + ' minutes'
        
        fields = [
            ('MEMBER COUNT', str(len(guild.members)), True),
            ('CREATED ON', creation_date[9:-8], True),
            ('OWNER', '<@{}>'.format(guild.owner.id), True),
            ('AFK TIMEOUT', afk_text, True),
            ('VOICE REGION', str(guild.region), True),
            ('ICON URL', '[Link]({})'.format(guild.icon_url), True),
            ('INVITE LINK', 'https://discord.gg/gCpJ9BF', False),
        ]
        
        for z in fields:
            slate.add_field(name=z[0], value=z[1], inline=z[2])
            
        slate.set_thumbnail(url=guild.icon_url)
        slate.set_footer(text='GUILD ID: {}'.format(guild.id))
        
        await ctx.send(embed=slate)
        
        
    @commands.command()
    async def about(self, ctx):
        user = self.bot.user
        creation_date = await self.convert_datetime(user.created_at)
        
        desc = 'Hi! I am a bot created and maintained by <@{}> for the /r/Malaysia Discord server.\n\n'.format(266107973128945664)
        
        desc += '**BACKGROUND**\n'
        desc += '`Username      : {}`\n'.format(str(user))
        desc += '`Username ID   : {}`\n'.format(user.id)
        desc += '`Creation Date : {}`\n\n'.format(creation_date)
        
        desc += '**DEVELOPMENT\n**'
        desc += '`Language      : Python 3.6`\n'
        desc += '`Library       : discord.py 1.0.0a0`\n\n'
        
        slate = discord.Embed(description=desc, colour=7506394)
        
        fields = [
            ('AVATAR URL', '[Link]({})'.format(user.avatar_url), True),
            ('SOURCE CODE', '[Link](https://github.com/polar-rex/Polar-Bot)', True),
        ]
        
        for x in fields:
            slate.add_field(name=x[0], value=x[1], inline=x[2])
        
        slate.set_thumbnail(url=user.avatar_url)
            
        await ctx.send(embed=slate)
                    
                    
    @commands.command()
    async def nick(self, ctx, new_nick:str=None):
        if new_nick == None:
            await ctx.send('Usage: `+nick [new nickname]`')
            
        else:
            await ctx.author.edit(nick=new_nick)
            await ctx.send('Your display name has been changed to {}.'.format(new_nick))
           
           
    @commands.command()
    async def clearnick(self, ctx):
        await ctx.author.edit(nick=None)
        await ctx.send('Your display name has been reverted to {}.'.format(ctx.author.name))
               
        
def setup(bot):
    bot.add_cog(General(bot))