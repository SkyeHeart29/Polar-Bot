import asyncio
import discord
import datetime
import pytz
from discord.ext import commands


class Log:
    def __init__(self, bot):
        self.bot = bot
    
    
    async def member_check(self, member):
        if member.id == 386870126332608513:
            return True
        
        return False
    
    
    async def get_time(self):
        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Asia/Kuala_Lumpur")
        present = old_timezone.localize(datetime.datetime.now()).astimezone(new_timezone)
        text = present.strftime('%A %Y-%m-%d %H:%M:%S (UTC+8)')
        return text
       
       
    async def create_slate(self, desc, url):
        time = await self.get_time()
        slate = discord.Embed(colour=7506394, description=desc)
        slate.set_footer(text=time)
        slate.set_thumbnail(url=url)
        return slate
    
    
    async def find_channel(self, guild):
        for x in guild.channels:
            if x.id == 305972553954885632:
                return x
                
    
    async def on_message_delete(self, message):
        if await self.member_check(message.author):
            return
        
        username = str(message.author)
        username_id = message.author.id
        display_name = message.author.display_name
        content = message.content
        content_id = message.id
        channel_name = message.channel.name
        channel_id = message.channel.id
        
        if content == '':
            content = 'css\nno text found'
        
        text = ':wastebasket: **MESSAGE DELETED**'
        text += '\n`USERNAME     : {}`'.format(username)
        text += '\n`DISPLAY NAME : {}`'.format(display_name)
        text += '\n`CHANNEL      : {}`'.format(channel_name)
        text += '\n`USERNAME ID  : {}`'.format(username_id)
        text += '\n`CHANNEL ID   : {}`'.format(channel_id)
        text += '\n`MESSAGE ID   : {}`'.format(content_id)
        
        slate = await self.create_slate(text, message.author.avatar_url)
        slate.add_field(name='CONTENT', value='```{}```'.format(content), inline=False)
        
        channel = await self.find_channel(message.guild)
        await channel.send(embed=slate)
        
        
    async def on_message_edit(self, before, after):
        if await self.member_check(after.author):
            return
            
        username = str(after.author)
        username_id = after.author.id
        display_name = after.author.display_name
        content_after = after.content
        content_before = before.content
        message_id = after.id
        channel_name = after.channel.name
        channel_id = after.channel.id
        
        if content_after == '':
            content_after = 'css\nno text found'
            
        if content_before == '':
            content_before = 'css\nno text found'
        
        text = ':pen_ballpoint: **MESSAGE EDITED**'
        text += '\n`USERNAME     : {}`'.format(username)
        text += '\n`DISPLAY NAME : {}`'.format(display_name)
        text += '\n`CHANNEL      : {}`'.format(channel_name)
        text += '\n`USERNAME ID  : {}`'.format(username_id)
        text += '\n`CHANNEL ID   : {}`'.format(channel_id)
        text += '\n`MESSAGE ID   : {}`'.format(message_id)
        
        slate = await self.create_slate(text, after.author.avatar_url)
        slate.add_field(name='BEFORE', value='```{}```'.format(content_before), inline=True)
        slate.add_field(name='AFTER', value='```{}```'.format(content_after), inline=True)
        
        channel = await self.find_channel(after.guild)
        await channel.send(embed=slate)
        
    
    async def on_member_join(self, member):
        text = '**:wave: MEMBER JOINED**'
        text += '\n`USERNAME      : {}`'.format(str(member))
        text += '\n`USERNAME ID   : {}`'.format(member.id)
        text += '\n`TOTAL MEMBERS : {}`'.format(len(member.guild.members))
        
        slate = await self.create_slate(text, member.avatar_url)
        channel = await self.find_channel(member.guild)
        await channel.send(embed=slate)
        
        
    async def on_member_remove(self, member):
        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Asia/Kuala_Lumpur")
        present = old_timezone.localize(member.joined_at).astimezone(new_timezone)
        joined_at = present.strftime('%A %Y-%m-%d %H:%M:%S (UTC+8)')
        
        text = '**:door: MEMBER REMOVED**'
        text += '\n`USERNAME      : {}`'.format(str(member))
        text += '\n`DISPLAY NAME  : {}`'.format(member.display_name)
        text += '\n`JOINED AT     : {}`'.format(joined_at)
        text += '\n`USERNAME ID   : {}`'.format(member.id)
        text += '\n`TOTAL MEMBERS : {}`'.format(len(member.guild.members))
        
        slate = await self.create_slate(text, member.avatar_url)
        channel = await self.find_channel(member.guild)
        await channel.send(embed=slate)
        
        
    async def on_member_ban(self, guild, user):
        text = '**:hammer: USER BANNED**'
        text += '\n`USERNAME      : {}`'.format(str(user))
        text += '\n`USERNAME ID   : {}`'.format(user.id)
        
        slate = await self.create_slate(text, user.avatar_url)
        channel = await self.find_channel(guild)
        await channel.send(embed=slate)
        

    async def on_member_unban(self, guild, user):
        text = '**:thumbsup: USER UNBANNED**'
        text += '\n`USERNAME      : {}`'.format(str(user))
        text += '\n`USERNAME ID   : {}`'.format(user.id)
        
        slate = await self.create_slate(text, user.avatar_url)
        channel = await self.find_channel(guild)
        await channel.send(embed=slate)
        
        
    async def on_member_update(self, before, after):
        if await self.member_check(after):
            return
            
        if before.display_name != after.display_name:
            text = ':dolls: **DISPLAY NAME CHANGED**'
            text += '\n`USERNAME         : {}`'.format(str(after))
            text += '\n`USERNAME ID      : {}`'.format(after.id)
            text += '\n`OLD DISPLAY NAME : {}`'.format(before.display_name)
            text += '\n`NEW DISPLAY NAME : {}`'.format(after.display_name)

            slate = await self.create_slate(text, after.avatar_url)
            channel = await self.find_channel(after.guild)
            await channel.send(embed=slate)
            
        if len(before.roles) < len(after.roles):
            for x in after.roles:
                if x not in before.roles:
                    text = ':unlock: **ROLE ASSIGNED**'
                    text += '\n`USERNAME      : {}`'.format(str(after))
                    text += '\n`DISPLAY NAME  : {}`'.format(after.display_name)
                    text += '\n`USERNAME ID   : {}`'.format(after.id)
                    text += '\n`ASSIGNED ROLE : {}`'.format(x.name)

                    slate = await self.create_slate(text, after.avatar_url)
                    channel = await self.find_channel(after.guild)
                    await channel.send(embed=slate)
                    
                    break
        
        if len(before.roles) > len(after.roles):
            for x in before.roles:
                if x not in after.roles:
                    text = ':closed_lock_with_key: **ROLE UNASSIGNED**'
                    text += '\n`USERNAME        : {}`'.format(str(after))
                    text += '\n`DISPLAY NAME    : {}`'.format(after.display_name)
                    text += '\n`USERNAME ID     : {}`'.format(after.id)
                    text += '\n`UNASSIGNED ROLE : {}`'.format(x.name)

                    slate = await self.create_slate(text, after.avatar_url)
                    channel = await self.find_channel(after.guild)
                    await channel.send(embed=slate)
                    
                    break
                    
        
def setup(bot):
    bot.add_cog(Log(bot))