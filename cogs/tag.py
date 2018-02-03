import asyncio
import discord
import rethinkdb as r
import time
from discord.ext import commands

class Tag:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_connection(self):
        return await r.connect("localhost", 28015, "tags")
    
    @commands.group(invoke_without_command=True, aliases=['t'])
    async def tag(self, ctx, tag:str, arg1:str="<arg1 missing>", arg2:str="<arg2 missing>"):
        conn = await self.get_connection()
        cursor = await r.table('tags').filter(r.row["tag"] == tag.lower()).run(conn)
        
        while (await cursor.fetch_next()):
            item = await cursor.next()
            formatting = {
                'tag': item['tag'],
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
            await r.table('tags').get(item['id']).update({'frequency': str(frequency + 1)}).run(conn)
        await conn.close()
        
    @tag.command()
    async def create(self, ctx, tag:str, content:str):
        if "@everyone" in content or "@here" in content:
            await ctx.send('Please do not put `@everyone` or `@here` in your tag.')
            return
            
        conn = await self.get_connection()
        await r.table('tags').insert({
            "tag": tag.lower(),
            "content": content,
            "owner": str(ctx.author.id),
            "created": str(time.time()),
            "last_edited": str(time.time()),
            "frequency": "0",
        }).run(conn)
        
        await ctx.send("Tag created.")
        await conn.close()
            
    @tag.command()
    async def list(self, ctx, member:discord.Member=None):
        conn = await self.get_connection()
        cursor = await r.table('tags').run(conn)
        
        if member == None:
            member = ctx.author
            
        owner = str(member.id)
        text = "{}'s tags:\n".format(member.display_name)
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item['owner'] == owner:
                text += "`{}`, ".format(item['tag'])
                
        to_send = text[:-2]
        await ctx.send(to_send)
        await conn.close()
        
    @tag.command()
    async def delete(self, ctx, tag:str):
        conn = await self.get_connection()
        cursor = await r.table('tags').filter(r.row["tag"] == tag.lower()).run(conn)
        
        while (await cursor.fetch_next()):
            item = await cursor.next()
            if item['owner'] == str(ctx.author.id):
                break
            else:
                await ctx.send("You are not the owner of this tag.")
                await conn.close()
                return
                
        await r.table('tags').filter(r.row["tag"] == tag.lower()).delete().run(conn)
        await ctx.send("Deleted `{}` successfully!".format(tag))
        await conn.close()
            
def setup(bot):
    bot.add_cog(Tag(bot))