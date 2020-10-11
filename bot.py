import discord
import time
import audioread
import pyttsx3
import sys

print('start')
engine = pyttsx3.init()

ffmpeg_path = "C:\\Users\\domin\\Documents\\ShareX\\Tools\\ffmpeg.exe"
who_where = dict()

async def record_and_play(voice, message):
    file_name = message + '.mp3'
    engine.save_to_file(message, file_name)
    engine.runAndWait()
    engine.stop()

    voice.play(discord.FFmpegPCMAudio(source = file_name, executable=ffmpeg_path))

    with audioread.audio_open(file_name) as f:
        time.sleep(f.duration)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        # if message.content == '$connect':
        #     self.voice_clienct = await self.connect_voice(message)

    async def on_voice_state_update(self, who, before, after):
        # print(who)
        # print(before)
        # print(after)

        if after.channel == None:
            await self.remove_name(before.channel, who)
        elif before.channel == None:
            await self.add_name(after.channel, who)
        else:
            await self.add_name(after.channel, who)

            if after.channel.name != before.channel.name:
                await self.remove_name(before.channel, who)

        print([[c, [x.name for x in who_where[c]]] for c in who_where])

    async def connect_voice(self, author, action, channel):
        if author.bot: return

        print(author)
        # guild = author.guild
        # channel = discord.utils.get(guild.channels, name = "AOE2")
        voice = await channel.connect()
        print(self)
        print(voice)
        voice_message = author.name + " " + action

        await record_and_play(voice, voice_message)
        await voice.disconnect()
        print('left ' + channel.name)

    async def remove_name(self, channel, who):
        return
        who_where[channel.name].remove(who)
        await self.connect_voice(who, 'left', channel)

    async def add_name(self, channel, who):
        if channel.name in who_where:
            who_where[channel.name].add(who)
        else:
            who_where[channel.name] = { who }
        await self.connect_voice(who, 'joined', channel)

client = MyClient()
client.run(sys.argv[1])

