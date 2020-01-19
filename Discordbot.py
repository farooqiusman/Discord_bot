import random
import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot  # importing the client
import urllib.parse, urllib.request, re
from discord import Game

BOT_PREFIX = ("?", "!")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Bot(command_prefix=BOT_PREFIX)  # creating the discord bot client and command prefix


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


@client.command(aliases=['hello'])
async def Greeting(context):
    await context.send("Hello! " + context.message.author.mention)


@client.command(aliases=['yo', 'Yo', 'YO'])
async def reply(ctx):
    possible_replies = [
        'nigga stfu',
        'who tf do you think you are',
        'I\'m sorry who are you',
        'It\'s all good here chief',
        'Your mom',
        'Ali don\'t like me',
        'Kevin is cool!',
        'Please die nigga',
        'I just want a body so I could kill you and your family',
    ]
    await ctx.send(random.choice(possible_replies))


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


#used to kill bot
@client.event
async def on_message(context):
	if context.author == client.user:
		return

	if context.content == '!stop':
		await client.logout()
#################################


@client.event
async def on_ready():
    game = discord.Game("with Zombies")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Logged in as " + client.user.name)


client.run(TOKEN)  # run command to tell client to run the discord bot
