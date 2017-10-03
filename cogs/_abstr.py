import asyncio
import discord
import random

async def postpages(bot, ctx, pages):
    # [⏪] fast-reverse   [◀] reverse   [▶] forward   [⏩] fast-forward   [🔢] random   [🗑] trash
    num = 0
    msg = await ctx.send(pages[num])
    
    for emoji in ['⏪', '◀', '▶', '⏩', '🔢', '🗑']:
        await msg.add_reaction(emoji)
    
    def check(reaction, user):
        return reaction.message.id == msg.id and user == ctx.author
    
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check, timeout=300.0)
        except:
            return
    
        emoji = reaction.emoji
        await msg.remove_reaction(emoji, ctx.author)

        if emoji == "⏪":
            num = 0
            
        if emoji == "◀":
            num -= 1
            
        if emoji == "▶":
            num += 1
            
        if emoji == "⏩":
            num = len(pages) - 1
            
        if emoji == "🔢":
            num = random.randint(0, len(pages) - 1)
            
        if emoji == "🗑":
            await msg.delete()
            return
        
        try:
            await msg.edit(content=pages[num])
        except:
            num = 0
            await msg.edit(content=pages[num])
            
def setup(bot):
    pass