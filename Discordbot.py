import random
import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot  # importing the client
import urllib.parse, urllib.request, re
from discord import Game
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord.utils import get

BOT_PREFIX = ("?", "!")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Bot(command_prefix=BOT_PREFIX)  # creating the discord bot client and command prefix


# Flipping a coin
@client.command()
async def flip(ctx):
    flip  = 0
    for i in range(10):
        flip = random.randint(0, 1)

    if (flip == 1):
        await ctx.send('https://media1.giphy.com/media/U6SqBmifGGHkae9JFQ/giphy-downsized-large.gif')
    else:
        await ctx.send('https://giphy.com/gifs/sonic-gifs-gif-ZRLdT8KRzdk4g')


# Q ball shit
@client.command(aliases=['8ball', 'eightball', '8-ball'])
async def eight_ball(context, *, question):
    possible_responses = [
        'That is a no',
        'Definitely',
        'Probably',
        'Too hard to tell',
        'Maybe',
    ]
    await context.send(f'Question: {question}\n Answer: {random.choice(possible_responses)}')


# Greeting
@client.command(aliases=['hello'])
async def Greeting(context):
    await context.send("Hello! " + context.message.author.mention)


# Replies
@client.command(aliases=['yo', 'Yo', 'YO'])
async def reply(ctx):
    possible_replies = [
        'Eva is not cool',
        'who tf do you think you are',
        'I\'m sorry who are you',
        'It\'s all good here chief',
        'Your mom',
        'Ali don\'t like me',
        'Kevin is cool!',
        'Ava is cool',
        'Faroochi and Ava shall rule this world!!!',
        'Pain :pain:',
        'I just want a body so I could kill you and your family',
        'My walls are green :pain:',
        'My uterine wall is shedding',
    ]
    await ctx.send(random.choice(possible_replies))

# youtube video
@client.command()
async def youtube(ctx, *, src):
    _str = urllib.parse.urlencode({
        'search_query': src
    })

    htm = urllib.request.urlopen(
        'http://www.youtube.com/results?' + _str
    )
    search_re = re.findall('href=\"\\/watch\\?v=(.{11})', htm.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_re[0])


# joining a voice channel
@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author))
        return
    else:
        channel = ctx.message.author.voice.channel
    
    await channel.connect()


# playing music
@client.command()
async def play(ctx, url):

    YDL_options = {'format':'bestaudio', 'noplaylist' : 'True'}
    FFMPEG_OPTIONS = {
        'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild = ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_options) as ydl:
            info = ydl.extract_info(url, download = False)

        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

    else:
        await ctx.send('Bot is already playing')
        return 

# pause music
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)
    
    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# resume music
@client.command()
async def resume(ctx): 
    voice = get(client.voice_clients, guild = ctx.guild)
    
    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is now resuming playback')

# stop music
@client.command()
async def stop(ctx): 
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Bot has stopped playback')

# discconect command
@client.command(aliases = ['dc', 'DC', 'Dc', 'fuckoff', 'leave'])
async def disconnect(ctx): 
    voice = get(client.voice_clients, guild = ctx.guild)
    await voice.disconnect(force = False)

# pain command
@client.command(aliases = ['PAIN', 'Pain'])
async def pain(ctx):
    with open('/home/usman/Documents/usman_pain.PNG', 'rb') as f:
        picture = discord.File(f)

    await ctx.send(file = picture)

#used to kill bot
# @client.event
# async def on_message(context):
# 	if context.author == client.user:
# 		return

# 	if context.content == '!stop':
# 		await client.logout()
#################################


@client.event
async def on_ready():
    game = discord.Game("Playing with Faroochi")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Logged in as " + client.user.name)


client.run(TOKEN)  # run command to tell client to run the discord bot
