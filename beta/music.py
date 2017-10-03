from __future__ import unicode_literals
import youtube_dl

import asyncio
import cogs._abstr as abstr
import discord
import os
import time
from discord.ext import commands

class Orb:
    def __init__(self, vc, tc, guild_id):
        self.songs = []
        self.vc = vc
        self.tc = tc
        self.guild_id = guild_id
        self.source = None
        self.switch = True
        self.skips = []

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.orbs = {}

    def extract_info(self, ctx, orb, song):
        r = None
        with youtube_dl.YoutubeDL(ydl_opts ={'ignoreerrors': True, 'default_search' : 'auto', 'quiet' : True}) as ydl:
            r = ydl.extract_info(song, download=False)
        
        to_iterate = []
        
        if 'entries' in r:  # if song is playlist.
            for video in r['entries']:
                if not video:
                    continue
                to_iterate.append(video)
            
        else:
            to_iterate.append(r)
        
        for video in to_iterate:
            entry = " **{0.get('title')}** uploaded by **{0.get('uploader')}** and requested by **{1.author.display_name}** [{0.get('duration')}s]".format(video, ctx)
            text = "Enqueued" + entry
            ctx.send(text)
            song_bag = (video.get('url'), entry)
            orb.songs.append(song_bag)

    def download(self, orb, url):
        ydl_opts = {
            'extract_audio' : True,
            'format' : 'bestaudio/best',
            'outtmpl' : 'audio/{}.%(ext)s'.format(orb.guild_id),
            'quiet': True,
            'ignoreerrors': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        for file in os.listdir('./audio'):
            if guild_id in file:
                return './audio/{}'.format(file), discord.FFmpegPCMAudio(file)
                
    def streamer(self, orb):
        while True:
            if orb.vc.is_playing() or orb.vc.is_paused():
                continue
            else:
                try:
                    song_bag = orb.songs.pop(0)
                    orb.tc.send("Downloading" + song_bag[1])
                    self.source, filename = self.download(orb, song_bag[0])
                    orb.tc.send("Now playing" + song_bag[1])
                    orb.vc.play(self.source)
                    orb.skips = []
                except:
                    start_time = time.time()
                    while True:
                        if orb.songs != []:
                            break
                        if time.time() - start_time > 300.0 or orb.switch == False:
                            orb.tc.send("Leaving voice chat.")
                            orb.vc.disconnect()
                            os.remove(filename)
                            self.orbs.remove(orb)
                            return
    
    @commands.command()
    async def play(self, ctx, *, song:str):
        loop = asyncio.get_event_loop()
        
        if ctx.author.voice.channel == None:
            await ctx.send("You're not in a voice channel!")
        
        if ctx.guild.id not in self.orbs:
            vc = ctx.author.voice.channel.connect(reconnect=True)
            orb = Orb(vc, ctx.message.channel, ctx.guild.id)
            self.orbs[ctx.guild.id] = orb
            loop.run_in_executor(None, self.streamer, self, orb)
        
        if ctx.guild.id in self.orbs:
            loop.run_in_executor(None, self.extract_info, self, ctx, self.orbs[ctx.guild.id], song)
            
    @commands.command()
    @commands.has_permissions(move_members=True)
    async def stop(self, ctx):
        orb = self.orbs(ctx.guild.id)
        orb.switch = False
        orb.songs = []
        orb.vc.stop()
    
    @commands.command()
    @commands.has_permissions(move_members=True)
    async def pause(self, ctx):
        vc = self.orbs[ctx.guild.id].vc
        vc.pause()
        await ctx.send("Paused.")
        
    @commands.command()
    @commands.has_permissions(move_members=True)
    async def resume(self):
        vc = self.orbs[ctx.guild.id].vc
        vc.pause()
        await ctx.send("Resumed")
        
    @commands.command()
    async def skip(self, ctx):
        orb = self.orbs[ctx.guild.id]
        if ctx.author.id not in orb.skips:
            orb.skips.append(ctx.author.id)
            
        else:
            await ctx.send("You've already added a skip.")
            
        total = len(orb.vc.channel.members) // 2 + 1
        await ctx.send("Number of skips: {}/{}".format(len(orb.skips),total))
        
        if len(orb.skips) >= total:
            orb.vc.stop()
            await ctx.send("Skipping song.")
        
    @commands.command()
    @commands.has_permissions(move_members=True)
    async def forceskip(self, ctx):
        orb = self.orbs[ctx.guild.id]
        if len(orb.skips) >= total:
            orb.vc.stop()
            await ctx.send("Skipping song.")
    
    @commands.command()
    async def playlist(self, ctx):
        pages = []
        unsorted = []
        
        for song_bag in self.orbs[ctx.guild.id].songs:
            unsorted.append(song_bag[1])
            await asyncio.sleep(0)
        
        count = 0
        while unsorted != []:
            text = "" #add skip count
            try:
                for x in range(10):
                    text += "[**{}**] {}\n".format(count+x, (unsorted.pop(0)))
                    await asyncio.sleep(0)
            except:
                pass
            pages.append(text)
            count += 10
            await asyncio.sleep(0)
            
        await abstr.postpages(self.bot, ctx, pages)
        
def setup(bot):
    bot.add_cog(Music(bot))