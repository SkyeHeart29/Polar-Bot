import cogs._abstr as abstr
import aiohttp
import asyncio
import bs4
import discord
from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot
        
        
    async def get_connection(self):
        return await r.connect("localhost", 28015)

        
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
    async def source(self, ctx):
        await ctx.send("https://github.com/polar-rex/Polar-Bot
        
        
    @commands.command()
    async def info(self, ctx, person:discord.Member=None):
        if person == None:
            person = ctx.author
        avatar
        await ctx.send(avatar)
        
        
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