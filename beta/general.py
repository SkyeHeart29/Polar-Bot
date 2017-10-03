import discord
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connections(self, ctx):
        await ctx.send("I'm in {} servers.".format(len(self.bot.guilds)))

    @commands.command()
    async def help(self, ctx):
        await ctx.send("https://gist.github.com/polar-rex/e0ff3188b5478930782b299be52ecb8d")

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?client_id=294708056112234497&scope=bot&permissions=1610083446")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")
    
    @commands.command()
    async def server(self, ctx):
        await ctx.send("https://discord.gg/5cxuTyN")
        
def setup(bot):
    bot.add_cog(General(bot))