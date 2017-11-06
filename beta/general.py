import discord
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connections(self, ctx):
        await ctx.send("I'm in {} servers.".format(len(self.bot.guilds)))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?client_id=294708056112234497&scope=bot&permissions=406121544&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Fpolar-rex%2FPolar-Bot")

    @commands.command()
    async def help(self, ctx):
        await ctx.send("https://github.com/polar-rex/Polar-Bot")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")
    
    @commands.command()
    async def server(self, ctx):
        await ctx.send("https://discord.gg/5cxuTyN")
        
def setup(bot):
    bot.add_cog(General(bot))