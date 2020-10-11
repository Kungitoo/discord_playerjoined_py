import discord
import time
import audioread
import pyttsx3
import sys

print('start')
engine = pyttsx3.init()

voice = None
async def get_voice(channel):
    if voice != None: 
        return voice
    return await channel.connect()

## Needs a path to ffmpeg.exe from the disk. Not provided
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

    async def on_voice_state_update(self, who, before, after):

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

        voice = await get_voice(channel)
        print(author.display_name)
        username = author.display_name if author.display_name else author.name
        voice_message = username + " " + action

        await record_and_play(voice, voice_message)
        await voice.disconnect()

    async def remove_name(self, channel, who):
        who_where[channel.name].remove(who)
        await self.connect_voice(who, 'left', channel)

    async def add_name(self, channel, who):
        if channel.name in who_where:
            where = who_where[channel.name]
            if who in where:
                return
            where.add(who)
        else:
            who_where[channel.name] = { who }
        await self.connect_voice(who, 'joined', channel)

client = MyClient()
client.run(sys.argv[1])

