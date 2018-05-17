import cogs._abstr as abstr
import aiohttp
import asyncio
import bs4
import discord
import datetime
import pytz
import re
import random
from discord.ext import commands


class Recreational:
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def translate(self, ctx, text=None, destination=None, source=None):
        if text == None:
            mess = 'Usage: `+translate [text] (output language) (input language)`, '
            mess += 'where output language is English if not given and input language is automatically detected if not given.'
            mess += '\nSee https://cloud.google.com/translate/docs/languages on what to type as output/input language.'
            mess += '\n* Be sure to enclose `[text]` with quotation marks.'
            await ctx.send(mess)
            return
        
        translator = googletrans.Translator()
        
        if destination == None:
            translated = translator.translate(text)
            await ctx.send(translated.text)
            
        elif source == None:
            translated = translator.translate(text, dest=destination)
            await ctx.send(translated.text)
            
        else:
            translated = translator.translate(text, dest=destination, src=source)
            await ctx.send(translated.text)
            
            
    @commands.command()
    async def lmgtfy(self, ctx, query=None):
        if query == None:
            await ctx.send('Usage: `+lmgtfy [text]`')
            
        else:
            await ctx.send("http://lmgtfy.com/?q={}".format(query.replace(" ", "+")))
            
       
    @commands.command(aliases=['g'])
    async def google(self, ctx, query=None):
        if query == None:
            await ctx.send('Usage: `+google [text]`')
            
        else:
            await ctx.send("http://google.com/search?q={}".format(query.replace(" ", "+")))
            
            
    @commands.command()
    async def convert(self, ctx, value=None, base='MYR', rate='USD'):
        if value == None:
            text = 'Usage: `+convert [value] (base) (rate)`\n\n'
            text += '`(base)` is MYR if not given.\n'
            text += '`(rate)` is USD if not given'
            await ctx.send(text)
            return
            
        fxrio = fixerio.Fixerio(base=rate.upper())
        table = fxrio.latest(base)
        weight = table['rates'][rate.upper()]
        number = float(value)
        result = number * weight
        
        await ctx.send('{} {} = {} {}'.format(number, base.upper(), result, rate.upper()))
        
        
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
    async def me(self, ctx, text:str=None):
        if text == None:
            await ctx.send('Usage: `+me [text]`')
            return
            
        await ctx.message.delete()
        name = ctx.author.display_name
        await ctx.send("* {} {}".format(name, text))
        
        
    @commands.command()
    async def kamus(self, ctx, search:str=None):
        if search == None:
            await ctx.send('Usage: `+kamus [word]`')
            return
            
        async with aiohttp.ClientSession() as session:
            async with session.get("http://prpm.dbp.gov.my/Cari1?keyword={}".format(search.replace(" ", "+"))) as resp:
                to_parse = await resp.text()
                soup = bs4.BeautifulSoup(to_parse, "html.parser")
                elements = soup.select(".tab-pane.fade.in.active")
                
                if elements == []:
                    await ctx.send('Kata {} tidak didapati dalam kamus'.format(search))
                
                for element in elements:
                    to_post = element.text
                    
                    v = re.compile('Definisi : (.*)')
                    mo = v.search(to_post)
                    text = mo.group()[11:]
                    await ctx.send(text)
                    
                    
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


    @commands.command()
    async def roll(self, ctx, number=None):
        if number == None:
            await ctx.send('Usage: `+roll [number larger than 2]`')
            return
            
        try:
            if int(number) < 2:
                await ctx.send('Number must be 2 or larger.')
                return
                
            result = random.randint(1, int(number) + 1)
            await ctx.send(result)
            
        except:
            await ctx.send('Input must be a number.')
            

    @commands.command()
    async def random(self, ctx, A=None, B=None):
        if A == None or B == None:
            await ctx.send('Usage: `+random [lowest number] [highest number]`')
            return
            
        try:
            result = random.randint(int(A), int(B) + 1)
            await ctx.send(result)
            
        except:
            await ctx.send('Input must be a number.')
            
            
    @commands.command()
    async def choose(self, ctx, *, items=None):
        if items == None:
            await ctx.send('Usage: `+choose [list of words seperated by spaces]`')
            return
            
        items = items.split(' ')
        choice = random.choice(items)
        await ctx.send(choice)
        
        
def setup(bot):
    bot.add_cog(Recreational(bot))