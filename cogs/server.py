import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Server:
    def __init__(self, bot):
        self.bot = bot
        
    async def get_connection(self):
        return await r.connect("localhost", 28015, 'bot')
        
    @commands.command()
    async def malaysian(self, ctx):
        for role in ctx.guild.roles:
            if role.name == "Malaysians":
                await ctx.author.add_roles(role)
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await ctx.send(item['rm1'])
                await conn.close()
                break
        for erase in ctx.author.roles:
            if erase.name == "Non-Malaysians":
                await ctx.author.remove_roles(erase)
                break
        
    @commands.command()
    async def nonmalaysian(self, ctx):
        for role in ctx.guild.roles:
            if role.name == "Non-Malaysians":
                await ctx.author.add_roles(role)
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await ctx.send(item['rm1'])
                await conn.close()
                break
        for erase in ctx.author.roles:
            if erase.name == "Malaysians":
                await ctx.author.remove_roles(erase)
                break
        
    @commands.command()
    async def pawagam(self, ctx):
        for erase in ctx.author.roles:
            if erase.name == "pawagam":
                await ctx.author.remove_roles(erase)
                return
        for role in ctx.guild.roles:
            if role.name == "pawagam":
                await ctx.author.add_roles(role)
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await ctx.send(item['rm2'])
                await conn.close()
                return
                
    @commands.command()
    async def pondok(self, ctx):
        for erase in ctx.author.roles:
            if erase.name == "pondok":
                await ctx.author.remove_roles(erase)
                return
        for role in ctx.guild.roles:
            if role.name == "pondok":
                await ctx.author.add_roles(role)
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await ctx.send(item['rm3'])
                await conn.close()
                return
                
    @commands.command()
    async def serious(self, ctx):
        for erase in ctx.author.roles:
            if erase.name == "serious":
                await ctx.author.remove_roles(erase)
                return
        for role in ctx.guild.roles:
            if role.name == "serious":
                await ctx.author.add_roles(role)
                conn = await self.get_connection()
                cursor = await r.table('bot').run(conn)
                while (await cursor.fetch_next()):
                    item = await cursor.next()
                    await ctx.send(item['rm4'])
                await conn.close()
                return
        
    @commands.command(aliases=['c'])
    async def colour(self, ctx, colour:str=None):
        colours = {
            'black': '000000',
            'blue': '1e90ff',
            'blueviolet': '8a2be2',
            'brown': '8b4513',
            'cyan': '00ffff',
            'darkblue': '0000cd',
            'darkgreen': '008000',
            'green': '00cd00',
            'indigo': '4b0082',
            'lightblue': 'add8e6',
            'magenta': 'ff00ff',
            'orange': 'cd8500',
            'purple': '800080',
            'pink': 'eea9b8',
            'red': 'ff0000',
            'turquoise': '00c5cd',
            'violet': 'd02090',
            'yellow': 'ffff00',
        }
        if colour == None:
            text = ""
            for key, value in colours.items():
                text += "`#{}` - *{}*\n".format(value, key)
                await asyncio.sleep(0)
            text += "\nContoh/Example: `+colour blue`"
            await ctx.send(text)
            return
        
        colour = colour.lower()
        if colour not in colours:
            await ctx.send("Invalid colour")
            return
            
        if colour in colours:
            for x in ctx.author.roles:
                if x.name in colours:
                    await ctx.author.remove_roles(x)
                    continue
            for y in ctx.guild.roles:
                if y.name == colour:
                    await ctx.author.add_roles(y)
                    await ctx.send("Warna nama anda sudah ditukar. The colour of your name has been changed.")
                    continue
            return
                    
def setup(bot):
    bot.add_cog(Server(bot))