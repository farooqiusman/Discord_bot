import random
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot  # importing the client
import urllib.parse, urllib.request, re
from discord import Game
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord.utils import get
import asyncio
from PIL import Image, ImageDraw
import re


BOT_PREFIX = ("?")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Bot(command_prefix=BOT_PREFIX)  # creating the discord bot client and command prefix
client.remove_command("help")


help_dict = {
    "flip" : "?flip-a-coin\n\tFlips a coin",
    "eight_ball" : "?8ball, !eight_ball, !8-ball <question>\n\tReturns an answer to a question",
    "reply" : "?reply\n\tWill return a random reply from the bot",
    "help" : "?hep\n\tWill display the help tab",
    "mock" : "?mock <text>\n\tWill return the inputted string with random upper-case/lower-case letters",
    "Greeting" : "?Greeting, ?hello\n\tWill have the bot say hello back to you",
    "join" : "?join\n\tWill have the bot join a voice channel",
    "play" : "?play <youtube url>\n\tWill have the bot play a song from youtube",
    "pause" : "?pause\n\tWill pause the current playback",
    "stop" : "?stop\n\tWill stop the current playback",
    "disconnect" : "?disconnect\n\tWill disconnect the bot from the voice channel",
    "resume" : "?resume\n\tWille resume the current playback",
    "update" : "?update/UP/EP <amount>\n\tWill update the points for person",
    "points" : "?points <amount>\n\tWill send a screen shot of the updated points for both members in server",
    "pain" : "?pain \n\tWill send a painful picture of usman to describe how much pain one is in",
    "motto" : "?mott\n\tWill display the server motto"
}


def getCharacters(digits):
    return len(str(digits))

def mockConverter(message):
    newString = ""
    for i in message:
        newString += i.upper() if random.randint(0, 1) == 1 else i.lower()
    return newString


# Flipping a coin
@client.command()
async def flip(ctx):
    await ctx.send("https://media1.giphy.com/media/U6SqBmifGGHkae9JFQ/giphy-downsized-large.gif" if random.randint(1, 100) <= 50 else 'https://giphy.com/gifs/sonic-gifs-gif-ZRLdT8KRzdk4g')

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
    await context.send(f'Question: {question}\nAnswer: {random.choice(possible_responses)}')


# Greeting
@client.command(aliases=['hello'])
async def Greeting(context):
    await context.send("Hello! " + context.message.author.mention)

# Ping
@client.command()
async def ping(ctx):
    await ctx.send(f"Latency: {round(client.latency * 1000)}ms")

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
        'Eva is very very hot',
        'Usman is very very sexy',
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

# disconnect command
@client.command(aliases = ['dc', 'DC', 'Dc', 'fuckoff', 'leave'])
async def disconnect(ctx): 
    voice = get(client.voice_clients, guild = ctx.guild)
    await voice.disconnect(force = False)

# pain command
@client.command(aliases = ['PAIN', 'Pain'])
async def pain(ctx):
    with open('usman_pain.png', 'rb') as f:
        picture = discord.File(f)

    msg = await (ctx.message.channel).fetch_message(ctx.message.id)
    await msg.delete()
    await ctx.send(file = picture)

# on ready
@client.event
async def on_ready():
    game = discord.Game("with Faroochi and Ava")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Logged in as " + client.user.name)


# clear
@client.command(aliases = ['snap'])
@commands.has_role("ADMIN")
async def clear(ctx, *, amount=1):
    await ctx.channel.purge(limit = amount + 1)

# boxed points system
@client.command()
async def points(ctx):
    f = open('/home/farooqi/Desktop/points.txt', "r")
    list = f.read().split('\n')
    list = list[:-1]
    f.close()
    num = 12 + getCharacters(list[0]) + getCharacters(list[1])
    diff = num - 12
    spaceDiff = 48 + diff
    under_score = ('_' * (50 + diff))

    space_before = (' ' * (int((spaceDiff - num)/2 - 1)))

    space_after = (' ' * (int((spaceDiff - num)/2 - 1)))

    under_score_inbetween = (' ' * (48 + diff))

    underscore_after = ('_' * (48 + diff))
    img = Image.new('RGB', ((330 + diff*10),100), color = (54, 56, 63))
    d = ImageDraw.Draw(img)


    text = ('   The current points for Ava and Faroochi are as follows: \n'
                   + '   ' + under_score + '\n'
                   + '   |' + under_score_inbetween + '|\n' 
                   + '   |' + space_before + 'Eva: ' + str(list[0]) + ', Usman: ' + str(list[1])
                   + space_after + '|\n' 
                   + '   |' + underscore_after + '|\n')

    d.text((10,10), text, fill=(255,255,255))
    img.save('save.png')
    await ctx.send(file=discord.File('save.png'))

# points
@client.command(aliases = ['UP', 'usmanpoints', 'EP', 'ep', 'up'])
async def update(ctx, amounts):
    user = ctx.message.author
    authorname = str(user)[0:str(user).index('#')]
    
    f = open('/home/farooqi/Desktop/points.txt', "r")
    list = f.read().split('\n')
    list = list[:-1]
    f.close()
    opp = None
    if authorname == 'Chobaka78': 
        opp = "Ava"
        with open('/home/farooqi/Desktop/points.txt', 'r+') as f:
            text = f.read()
            text = re.sub(str(list[0]), str(int(list[0]) + int(amounts)), text)
            f.seek(0)
            f.write(text)
            f.truncate()

        f.close()

    elif authorname == 'eva':
        opp = "Faroochi"
        with open('/home/farooqi/Desktop/points.txt', 'r+') as f:
            text = f.read()
            text = re.sub(str(list[1]), str(int(list[1]) + int(amounts)), text)
            f.seek(0)
            f.write(text)
            f.truncate()

        f.close()

    await ctx.send("Amount: " + str(amounts) + " added to " + opp)


# mockconverter
@client.command()
async def mock(ctx, *, message):
    newString = mockConverter(message)
    msg = await (ctx.message.channel).fetch_message(ctx.message.id)
    await msg.delete()
    await ctx.send(newString)

# help
@client.command()
async def help(ctx, *, command=None):
    embed = discord.Embed(title="HELP", colour=0xff1333)
    if command is None:
        for i in help_dict:
            embed.add_field(name=i, value=help_dict[i], inline=False)
    elif command in help_dict:
        embed.add_field(name=command, value=help_dict[command], inline=False)
    else:
        await ctx.send("This command does not exist")
        return
    await ctx.send(embed=embed)

@client.command()
async def motto(ctx):
    await ctx.send("```Server motto: \n-Always head\n-Always forgive\n-Always b safe\n-Always hugs\n-Always speak before you think\n-Always b strong\n```")


client.run(TOKEN)  # run command to tell client to run the discord bot
