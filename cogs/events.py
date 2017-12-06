import asyncio
import discord
import rethinkdb as r
from discord.ext import commands

class Events:
    def __init__(self, bot):
        self.bot = bot

    async def get_connection(self):
        return await r.connect("localhost", 28015)
        
    async def on_ready(self):
        print("Logged in!")
        print("Name: %s" % self.bot.user.name)
        print("ID: %s" % self.bot.user.id)
        print("Discord API version: {}".format(discord.__version__))
        
        await self.bot.change_presence(game=discord.Game(name="in the Arctic."))
    
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
        else:
            await ctx.send("ERROR:```{}```".format(e))
            
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if channel.id == 292555897820020740:
                await channel.send("Selamat sejahtera, <@{}> ke **server Discord /r/Malaysia**! Sila baca peraturan di #about dan taip `+malaysian` atau `+nonmalaysian` untuk mendapatkan peranan. Harap anda berseronok di sini.<:najib:292879676198879232><:tehtarik:361901626295975936>\n\nWelcome, <@{}> to **/r/Malaysia's Discord server**! Please read the rules in #about and type `+malaysian` or `nonmalaysian` to get a role. Don't forget to have a good time.<:najib:292879676198879232><:tehtarik:361901626295975936>".format(member.id, member.id))
                return
        
def setup(bot):
    bot.add_cog(Events(bot))