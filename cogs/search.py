import cogs._abstr as abstr
import aiohttp
import asyncio
import bs4
import discord
from discord.ext import commands

class Search:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['youtube'])
    async def yt(self, ctx, *, search:str):
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
    bot.add_cog(Search(bot))