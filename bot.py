import asyncio
import discord
import logging
import os
import rethinkdb as r
import sys
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

r.set_loop_type('asyncio')

async def get_connection():
    return await r.connect("localhost", 28015)
        
async def get_pre(bot, message):
    conn = await get_connection()
    guild_id = str(message.guild.id)
    bot_id = str(bot.user.id)
    
    if bot_id+guild_id not in await r.db('properties').table_list().run(conn):
        await r.db('properties').table_create(bot_id+guild_id).run(conn)
        await r.db('properties').table(bot_id+guild_id).insert({
            "prefix": ".",
        }).run(conn)
        
    cursor = await r.db("properties").table(bot_id+guild_id).run(conn)
    while (await cursor.fetch_next()):
        item = await cursor.next()
        return item["prefix"]

bot = commands.Bot(command_prefix=get_pre)
bot.remove_command("help")
cogs = []

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
            if file == "__pycache__":
                continue
            cog_name = "{}.{}".format(folder, file[:-3])
            cogs.append(cog_name)
            bot.load_extension(cog_name)
            print("Loaded {}".format(cog_name))
    except:
        pass
    
    bot.run(sys.argv[1])