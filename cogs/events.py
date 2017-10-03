import discord
from discord.ext import commands

class Events:
    def __init__(self, bot):
        self.bot = bot
        
    async def on_ready(self):
        print("Logged in!")
        print("Name: %s" % self.bot.user.name)
        print("ID: %s" % self.bot.user.id)
        print("Discord API version: %s" % discord.__version__)
        await self.bot.change_presence(game=discord.Game(name='in the Arctic. Ping me.'))
    
    async def on_guild_join(self, guild):
        if len(self.bot.guilds) > 100:
            for channel in guild.channels:
                try:
                    await channel.send("Sorry, I can't join any more servers. Maybe next time when I can.")
                    break
                except:
                    pass
            await guild.leave()
    
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.content == "<@{}>".format(self.bot.user.id):
            await message.channel.send("Call my commands by pinging me or using the full-stop prefix.\n\nhttps://gist.github.com/polar-rex/e0ff3188b5478930782b299be52ecb8d")
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
        else:
            await ctx.send("An error has occured. Report to The Arctic Den. (Type `.server` for the link) ```{}```".format(e))
        
def setup(bot):
    bot.add_cog(Events(bot))