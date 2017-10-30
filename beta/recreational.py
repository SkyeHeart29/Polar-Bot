import discord
from discord.ext import commands

class Recreational:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def me(self, ctx, *, text:str):
        await ctx.message.delete()
        name = ctx.author.display_name
        await ctx.send("* {} {}".format(name, text))
        
def setup(bot):
    bot.add_cog(Recreational(bot))