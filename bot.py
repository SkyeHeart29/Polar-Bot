import asyncio
import discord
import logging
import sys
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description='A polar bear robot')
bot.remove_command("help")

@bot.command()
@commands.is_owner()
async def load(ctx, extension:str):
    bot.load_extension(extension)
    await ctx.send("`{}` extension has been loaded.".format(extension))
    cogs.append(extension)

@bot.command()
@commands.is_owner()
async def unload(ctx, extension:str):
    bot.unload_extension(extension)
    await ctx.send("`{}` extension has been unloaded.".format(extension))
    cogs.remove(extension)
    
@bot.command()
@commands.is_owner()
async def reload(ctx, extension:str):
    await ctx.invoke(unload, extension)
    await ctx.invoke(load, extension)
    
@bot.command()
@commands.is_owner()
async def extensions(ctx):
    text = ""
    for cog in cogs:
        text += cog + "\n"
        await asyncio.sleep(0)
    await ctx.send(text)
    
if __name__ == "__main__":
    folder = input("Load cogs from: ")
    try:
        for file in os.listdir(folder):
            cog_name = "{}.{}".format(folder, file[:-4])
            bot.load_extension(cog_name)
            print("Loaded {}".format(cog_name))
    except:
        pass
        
    bot.run(sys.argv[1])