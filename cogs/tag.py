import asyncio
import discord
import rethinkdb as r
import time
from discord.ext import commands

class Tag:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_connection(self):
        return await r.connect("localhost", 28015)
    
    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx, tag_name:str, arg1:str="<arg1 missing>", arg2:str="<arg2 missing>"):
        conn = await self.get_connection()
        cursor = await r.db('tags').table(str(ctx.guild.id)).filter(r.row["tag_name"] == tag_name.lower()).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            formatting = {
                'tag': item['tag_name'],
                'me': ctx.author.display_name,
                'me-username': ctx.author.name,
                'me-user': str(ctx.author),
                'me-discrim': ctx.author.discriminator,
                'me-id': ctx.author.id,
                'channel': ctx.message.channel.name,
                'channel-id': ctx.message.channel.id,
                'server': ctx.guild.name,
                'server-id': ctx.guild.id,
                'freq': item['frequency'],
                'arg1': arg1,
                'arg2': arg2,
            }
            await ctx.send(item['content'].format(**formatting))
            frequency = int(item['frequency'])
            await r.db('tags').table(str(ctx.guild.id)).get(item['id']).update({'frequency': str(frequency + 1)}).run(conn)            
        
    @tag.command()
    async def create(self, ctx, tag_name:str, *, content:str=None):
        conn = await self.get_connection()
        if content == None:
            await ctx.send("You need to add some content!")
            return
        elif "@everyone" in content or "@here" in content:
            await ctx.send('Please do not put `@everyone` or `@here` in your tag.')
            return
        else:
            guild_id = str(ctx.guild.id)
            
            if guild_id not in await r.db('tags').table_list().run(conn):
                await r.db('tags').table_create(guild_id).run(conn)
                
            await r.db('tags').table(guild_id).insert({
                "tag_name": tag_name.lower(),
                "content": content,
                "spoiler": False,
                "owner": str(ctx.author.id),
                "created": str(time.time()),
                "last_edited": str(time.time()),
                "frequency": "0",
                "nsfw": False
            }).run(conn)
            
            await ctx.send("Your tag has been added!")
            
    @tag.command()
    async def list(self, ctx, member:discord.Member=None):
        conn = await self.get_connection()
        cursor = await r.db('tags').table(str(ctx.guild.id)).run(conn)
        if member == None:
            member = ctx.author
        owner = str(member.id)
        text = "{}'s tags:\n".format(member.display_name)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item['owner'] == owner:
                text += "`{}`, ".format(item['tag_name'])
        if len(text) > 2000:
            await ctx.send("Too many tags to display.")
            return
        else:
            to_send = text[:-2]
            await ctx.send(to_send)
        
    @tag.command()
    async def delete(self, ctx, tag_name:str):
        conn = await self.get_connection()
        cursor = await r.db('tags').table(str(ctx.guild.id)).filter(r.row["tag_name"] == tag_name.lower()).run(conn)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item['owner'] == str(ctx.author.id):
                break
            else:
                await ctx.send("You are not the owner of this tag.")
                return
        await r.db('tags').table(str(ctx.guild.id)).filter(r.row["tag_name"] == tag_name.lower()).delete().run(conn)
        await ctx.send("Deleted `{}` successfully!".format(tag_name))
            
def setup(bot):
    bot.add_cog(Tag(bot))