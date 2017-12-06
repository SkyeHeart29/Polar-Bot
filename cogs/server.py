import asyncio
import discord
from discord.ext import commands

class Server:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def malaysian(self, ctx):
        for role in ctx.guild.roles:
            if role.name == "Malaysians":
                await ctx.author.add_roles(role)
                break
        for erase in ctx.author.roles:
            if erase.name == "Non-Malaysians":
                await ctx.author.remove_roles(erase)
                break
        await ctx.send("Peranan diberikan. Anda boleh tukar warna nama anda. Taip `+colour` of mengetahui kelanjutan.\n\nRole given. You can change the colour of your name. Type `+colour` to know more.")
        
    @commands.command()
    async def nonmalaysian(self, ctx):
        for role in ctx.guild.roles:
            if role.name == "Non-Malaysians":
                await ctx.author.add_roles(role)
                break
        for erase in ctx.author.roles:
            if erase.name == "Malaysians":
                await ctx.author.remove_roles(erase)
                break
        await ctx.send("Peranan diberikan. Anda boleh tukar warna nama anda. Taip `+colour` of mengetahui kelanjutan.\n\nRole given. You can change the colour of your name. Type `+colour` to know more.")
        
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