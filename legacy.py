import asyncio
import discord
import sys
from discord.ext import commands

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '**{0.title}** uploaded by **{0.uploader}** and requested by **{1.display_name}**'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.playlist = []

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
            self.playlist.pop(0)

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)
            state.playlist.append(str(entry))

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(deafen_members=True)
    async def volume(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(deafen_members=True)
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(deafen_members=True)
    async def resume(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(deafen_members=True)
    async def stop(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass
            
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_permissions(deafen_members=True)
    async def forceskip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        await self.bot.say("Skipping song...")
        state.skip()

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            max_votes = len(state.voice.channel.voice_members) // 2
            if total_votes >= max_votes:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/{}]'.format(total_votes, max_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playlist(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            max_votes = len(state.voice.channel.voice_members) // 2
            
            copy = state.playlist
            
            def chunks(l, n):
                for i in range(0, len(l), n):
                    yield l[i:i + n]
            
            raw = list(chunks(copy, 10))
            pages = []
            ten = 0
            
            for chunk in raw:
                text = "Now playing {} [skips: {}/{}]\n".format(state.current, skip_count, max_votes)
                await asyncio.sleep(0)
                for index, value in enumerate(chunk):
                    text += "[{}] - {}\n".format(index+ten, value)
                    await asyncio.sleep(0)
                pages.append(text)
                ten += 10
            
            num = 0
            msg = await self.bot.say(pages[num])
    
            for emoji in ['⏪', '◀', '▶', '⏩', '🔢', '🗑']:
                await self.bot.add_reaction(msg, emoji)
    
            while True:
                try:
                    reaction, user = await bot.wait_for_reaction(emoji=['⏪', '◀', '▶', '⏩', '🔢', '🗑'], user=ctx.message.author, timeout=300.0, message=msg)
                except:
                    return
    
                emoji = reaction.emoji
                await bot.remove_reaction(msg, emoji, ctx.message.author)

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
                    await self.bot.delete_message(msg)
                    return
        
                try:
                    await bot.edit_message(msg, new_content=pages[num])
                except:
                    num = 0
                    await bot.edit_message(msg, new_content=pages[num])
                
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

prefix = "."
description = "A polar bear robot that does things!"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description=description)
bot.remove_command("help")
bot.add_cog(Music(bot))
        
bot.run(sys.argv[1])