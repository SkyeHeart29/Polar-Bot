import asyncio
import discord
import datetime
import pytz
import rethinkdb as r
from discord.ext import commands


class Mod:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member):
        def check(message):
            return message.author == ctx.author
            
        await ctx.send("Are you sure you want to ban **{}**? Type `yes` or `no`.".format(str(member)))
        msg1 = await self.bot.wait_for('message', check=check)
        
        if msg1.content.lower() != 'yes':
            await ctx.send("Command terminated.")
            return
    
        await ctx.send("Reason?")
        reason = await self.bot.wait_for('message', check=check)
        
        await ctx.send("Delete how many days' worth of messages? (0-7)")
        delete_message_days = await self.bot.wait_for('message', check=check)
        
        await member.ban(reason=reason.content, delete_message_days=int(delete_message_days.content))
        await ctx.send("Success!")
        
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx):
        bans = await ctx.guild.bans()
        text = 'Type in a number:\n'
        
        for x, y in enumerate(bans):
            text += '\n`{} - {}`'.format(x, str(y[1]))
        
        def check(message):
            return message.author == ctx.author
        
        await ctx.send(text)
        msg0 = await self.bot.wait_for('message', check=check)
        
        if msg0.content.isdigit() == False:
            await ctx.send("Invalid input. Try again.")
            return
            
        if int(msg0.content) not in list(range(len(bans))):
            await ctx.send("Invalid number. Try again.")
            return
        
        await ctx.send("Are you sure you want to unban **{}**? Type `yes` or `no`.".format(str(bans[int(msg0.content)][1])))
        msg1 = await self.bot.wait_for('message', check=check)
        
        if msg1.content.lower() != 'yes':
            await ctx.send("Command terminated.")
            return
    
        await ctx.send("Reason?")
        reason = await self.bot.wait_for('message', check=check)
        
        await ctx.guild.unban(user=bans[int(msg0.content)][1] ,reason=reason.content)
        await ctx.send("Success!")
        
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, id:int=None):
        if id == None:
            await ctx.send('Usage: `+hackban [user ID]`')
            return
        
        def check(message):
            return message.author == ctx.author
            
        user = await self.bot.get_user_info(id)
        
        await ctx.send("Are you sure you want to ban **{}**? Type `yes` or `no`.".format(str(user)))
        msg1 = await self.bot.wait_for('message', check=check)
        
        if msg1.content.lower() != 'yes':
            await ctx.send("Command terminated.")
            return
    
        await ctx.send("Reason?")
        reason = await self.bot.wait_for('message', check=check)
        
        await ctx.send("Delete how many days' worth of messages? (0-7)")
        delete_message_days = await self.bot.wait_for('message', check=check)
        
        await ctx.guild.ban(user, reason=reason.content, delete_message_days=int(delete_message_days.content))
        await ctx.send("Success!")
            
            
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member):
        def check(message):
            return message.author == ctx.author
        
        await ctx.send("Are you sure you want to kick **{}**? Type `yes` or `no`.".format(str(member)))
        msg1 = await self.bot.wait_for('message', check=check)
        
        if msg1.content.lower() != 'yes':
            await ctx.send("Command terminated.")
            return
        
        await ctx.send("Reason?")
        reason = await self.bot.wait_for('message', check=check)
        
        await member.kick(reason=reason.content)
        await ctx.send("Success!")
        
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, x):
        deleted_messages = await ctx.message.channel.purge(limit=int(x)+1)
        success_message = await ctx.send("Deleted {} messages. This message will self-destruct in 10 seconds...".format(len(deleted_messages)-1))
        await asyncio.sleep(10)
        await success_message.delete()
        
        
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def modnick(self, ctx, person:discord.Member=None, new_nick:str=None):
        if new_nick == None or person == None:
            await ctx.send('Usage: `+modnick [member] [new nickname]`')
            
        else:
            await person.edit(nick=new_nick)
            await ctx.send('{}\'s display name has been changed to {}.'.format(str(person), new_nick))
           
           
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def modclearnick(self, ctx, person:discord.Member=None):
        if person == None:
            await ctx.send('Usage: `+modclearnick [member]`')
        
        else:
            await person.edit(nick=None)
            await ctx.send('{}\'s display name has been reverted to {}.'.format(str(person), person.name))
               
        
def setup(bot):
    bot.add_cog(Mod(bot))