import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.roles = {
            'malaysian'     : 292540909336395776 ,
            'nonmalaysian'  : 292540989263052801 ,
            'boardgame'     : 398440186935246850 ,
            'muzium'        : 446517214523162624 ,
        }
        self.colours = {
            ('black', 'hitam')          : 300271837437231104 ,
            ('blue', 'biru')            : 301955358686052354 ,
            ('blueviolet', 'biruungu')  : 302732767421267969 ,
            ('brown', 'perang')         : 300271243280646145 ,
            ('cyan', 'biruhijau')       : 301956646706610177 ,
            ('darkblue', 'birutua')     : 300271731015417856 ,
            ('darkgreen', 'hijautua')   : 302732751193243648 ,
            ('green', 'hijau')          : 300269285140463627 ,
            ('indigo', 'birulaut')      : 300272462036336641 ,
            ('lightblue', 'birumuda')   : 300269518020673537 ,
            ('magenta', 'merahungu')    : 301956778453762049 ,
            ('orange', 'jingga')        : 300272031600082944 ,
            ('purple', 'ungu')          : 300270655457329152 ,
            ('pink', 'merahjambu')      : 300269738779607040 ,
            ('red', 'merah')            : 300270217874112513 ,
            ('turquoise', 'hijaubiru')  : 300269890927853568 ,
            ('violet', 'birumerah')     : 300272257069219841 ,
            ('white', 'putih')          : 444404468252016640 ,
            ('yellow', 'kuning')        : 300269629648142336 ,
        }
        
    async def postfile(self, filename):
        with open('./data/{}.txt'.format(filename)) as file:
            return file.read()
            
        
    async def get_connection(self):
        return await r.connect("localhost", 28015, 'bot')

        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def role_id(self, ctx):
        for x in ctx.guild.roles:
            await ctx.send('{} - **{}**'.format(x.id, x.name))
            
        
    @commands.command(aliases=['giveme', 'beri'])
    async def give(self, ctx, to_give=None):
        if (to_give == None) or (to_give == 'list'):
            text = 'Senarai Peranan/Role List:\n\n'
            
            for x in self.roles:
                text += '`{}`\n'.format(x)
            
            text += '\nContoh: `+beri malaysian`'
            text += '\nExample: `+give malaysian`'
            await ctx.send(text)
            return
        
        to_give = to_give.lower()
        if to_give not in self.roles:
            await ctx.send('Peranan tidak dijumpai. Role is not found.')
            return
            
        for x in ctx.author.roles:  # if member already has the role
            if int(x.id) == self.roles[to_give]:
                await ctx.author.remove_roles(x)
                text_1 = await self.postfile('role_removed')
                text_1 = text_1.format(ctx.author.id, x.name, x.name)
                await ctx.send(text_1)
                return
                          
        for y in ctx.guild.roles:   # add new role
            if y.id == self.roles[to_give]:
                await ctx.author.add_roles(y)
                text_2 = await self.postfile('role_given')
                text_2 = text_2.format(ctx.author.id, y.name, y.name)
                await ctx.send(text_2)
                return
        
        
    @commands.command(aliases=['color', 'warna'])
    async def colour(self, ctx, to_give:str=None):
        if (to_give == None) or (to_give == 'list'):
            text = 'Senarai peranan warna/List of colour roles:\n\n'
            
            for key, value in self.colours.items():
                text += "`{}`/`{}`\n".format(key[1], key[0])
                
            text += '\nContoh: `+warna biru`'
            text += '\nExample: `+colour blue`'
            await ctx.send(text)
            return
        
        to_give = to_give.lower()
        for key, value in self.colours.items():
            if to_give in key:
            
                for x in ctx.author.roles:  # if member already has the role
                    if x.id == value:
                        await ctx.author.remove_roles(x)
                        text_1 = await self.postfile('role_removed')
                        text_1 = text_1.format(ctx.author.id, x.name, x.name)
                        await ctx.send(text_1)
                        return
                        
                for a, b in self.colours.items():   # remove any existing colour role
                    for y in ctx.author.roles:
                        if y.id == b:
                            await ctx.author.remove_roles(y)
                            text_2 = await self.postfile('role_removed')
                            text_2 = text_2.format(ctx.author.id, y.name, y.name)
                            await ctx.send(text_2)
                            
                for p in ctx.guild.roles:   # add new role
                    if p.id == value:
                        await ctx.author.add_roles(p)
                        text_3 = await self.postfile('role_given')
                        text_3 = text_3.format(ctx.author.id, p.name, p.name)
                        await ctx.send(text_3)
                        return
        
        await ctx.send("Warna tiada dalam senarai. The colour is not in the list.")
        return
                 
                 
def setup(bot):
    bot.add_cog(Roles(bot))