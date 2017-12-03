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
        await ctx.send("Peranan diberikan. Role given.")
        
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
        await ctx.send("Peranan diberikan. Role given.")
        
def setup(bot):
    bot.add_cog(Server(bot))