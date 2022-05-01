import requests, json,asyncio, time, os
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
import discord
from gtts import gTTS
from pydub import AudioSegment

bot = commands.Bot(command_prefix='!')
config = json.load(open('config.json'))
token = config['token']
@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="!iss"))
    channel = discord.utils.get(bot.get_all_channels(), name="ISS POSITION")
    voice = await channel.connect()
    try:
        while True:
            if voice.is_playing() == False:
                url = "http://api.open-notify.org/iss-now.json"
                r = requests.get(url)
                data = r.json()
                lat = data['iss_position']['latitude']
                lon = data['iss_position']['longitude']
                now = datetime.now()
                time = now.strftime("%H:%M:%S")
                tts = gTTS(text=f"ISS Position Latitude {lat} Longtitude {lon} | Request time {time}", lang='en')
                tts.save("iss.mp3")
                iss = AudioSegment.from_mp3("iss.mp3")
                vhf = AudioSegment.from_mp3("VHF.mp3")
                output = iss.append(vhf, crossfade=200)
                output.export("iss.mp3", format="mp3")
                voice.play(discord.FFmpegPCMAudio("iss.mp3"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 100
            else:            
                print("", end="\r")
    except Exception as e:
        print(e)
       
bot.run(token)