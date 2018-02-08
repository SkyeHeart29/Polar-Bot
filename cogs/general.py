import cogs._abstr as abstr
import aiohttp
import asyncio
import bs4
import discord
import datetime
import pytz
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
     
     
    @commands.group(invoke_without_command=True)
    async def help(self, ctx, arg='help'):
        slate = discord.Embed(colour=7506394)
        terms = ['help', 'mod', 'tag', 'owner']
        
        if arg in terms:
            with open('./data/{}.txt'.format(arg)) as file:
                text = file.read()
                slate.description = text
            await ctx.send(embed=slate)
            
        else:
            await ctx.send('Invalid help page.')
        
        
    @commands.command()
    async def me(self, ctx, text:str=None):
        if text == None:
            await ctx.send('Usage: `+me [text]`')
            return
            
        await ctx.message.delete()
        name = ctx.author.display_name
        await ctx.send("* {} {}".format(name, text))

        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

        
    @commands.command()
    async def reverse(self, ctx, text:str=None):
        if text == None:
            await ctx/send('Usage: `+reverse [text]`')
            return
            
        text = text[::-1]
        await ctx.send(text)
        
        
    @commands.command()
    async def invert(self, ctx, text:str=None):
        if text == None:
            await ctx/send('Usage: `+invert [text]`')
            return
        
        ref_1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        ref_2 = 'ᗄᗷ⊂DEᖶ⅁HIᘃʞ⅂ʍNObⵚᖉᴤ⊥∩⋀MX⅄Zɐpⅽqөʈɓµ!ɾʞꞁwuobdʁƨʇ∩٨ʍxʎz0123456789'
        new_text = ''
        for x in text:
            if x in ref_1:
                for i, v in enumerate(ref_1):
                    if x == v:
                        new_text += ref_2[i]
                        break
                
            else:
                new_text += x
                
        await ctx.send(new_text)
        
        
    @commands.command()
    async def mirror(self, ctx, text:str=None):
        if text == None:
            await ctx/send('Usage: `+mirror [text]`')
            return
        
        ref_1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        ref_2 = 'AᙠƆᗡƎᖷᎮHIႱᐴ⅃MИOꟼỌЯƧTUVWXYƸɒdɔbɘʇǫʜiႱʞlmnoqpɿƨƚuvwxyz012Ƹ456789'
        new_text = ''
        for x in text[::-1]:
            if x in ref_1:
                for i, v in enumerate(ref_1):
                    if x == v:
                        new_text += ref_2[i]
                        break
                
            else:
                new_text += x
            
        await ctx.send(new_text)
        
        
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
    async def yt(self, ctx, *, search:str=None):
        if search == None:
            await ctx.send('Usage: `+yt [text]`')
            return
            
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.youtube.com/results?search_query={}".format(search.replace(" ", "+"))) as resp:
                to_parse = await resp.text()
                bs_object = bs4.BeautifulSoup(to_parse, "html.parser")
                elements = bs_object.select('div > h3 > a')
                links = []
                
                for ind, url in enumerate(elements):
                    links.append("[**{}**/{}] https://www.youtube.com{}".format(ind+1, len(elements), url['href']))
                    await asyncio.sleep(0)
                    
                await abstr.postpages(self.bot, ctx, links)
               
        
def setup(bot):
    bot.add_cog(General(bot))