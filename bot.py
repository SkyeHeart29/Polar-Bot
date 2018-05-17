import discord
import logging
import os
import rethinkdb as r
import sys
from discord.ext import commands


logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix="+")
bot.remove_command("help")
coglist = []


@bot.command()
@commands.is_owner()
async def load(ctx, cog:str):
    if cog in coglist:
        await ctx.send("Cog already loaded!")
        return
        
    bot.load_extension("cogs.{}".format(cog))
    await ctx.send("Loaded {}.".format(cog))
    coglist.append(cog)

    
@bot.command()
@commands.is_owner()
async def unload(ctx, cog:str):
    if cog not in coglist:
        await ctx.send("Cog was not loaded!")
        return
        
    bot.unload_extension("cogs.{}".format(cog))
    await ctx.send("Unloaded {}.".format(cog))
    coglist.remove(cog)

    
@bot.command()
@commands.is_owner()
async def reload(ctx, cog:str):
    if cog not in coglist:
        await ctx.send("Cog was not loaded!")
        return
        
    await ctx.invoke(unload, cog)
    await ctx.invoke(load, cog)
    
    
@bot.command()
@commands.is_owner()
async def cogs(ctx):
    text = ""
    for cog in coglist:
        text += cog + "\n"
        
    await ctx.send(text)
    
    
@bot.check
def check_commands(ctx):
    if ctx.guild == None:
        return False
        
    else:
        return True
    
if __name__ == "__main__":
    for file in os.listdir('cogs'):
        if file == "__pycache__" or file == "_abstr.py":
            continue
        bot.load_extension('cogs.{}'.format(file[:-3]))
        coglist.append(file[:-3])
        print("Loaded {}.".format(file[:-3]))
    r.set_loop_type('asyncio')
    bot.run(sys.argv[1])