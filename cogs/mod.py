import asyncio
import discord
from discord.ext import commands

class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member:discord.Member):
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
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, member:discord.Member):
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
        
def setup(bot):
    bot.add_cog(Mod(bot))