import discord
from discord.ext.commands import Bot
from discord.ext import  commands
import asyncio
import time
import os

Client = discord.Client()
bot = commands.Bot(command_prefix="-", pm_help = False)
bot.remove_command("help")

userList = []
elected = 0

@bot.event
async def on_ready():
    print("Bot is ready!")
    
@bot.command(pass_context=True)
async def join(ctx):
    user = ctx.message.author
    #user = str(author.name)
    if user not in userList:
        userList.append(user)    
    await sayList()

@bot.command(pass_context=True)
async def remove(ctx):
    user = ctx.message.author
    userList.remove(user)    
    await sayList()
    
@bot.command()
async def sing(*args):
    global elected
    elected = elected+1
    if elected >= len(userList):
        elected = 0
    await sayList()
    if len(userList) > 0:
        user = userList[elected]
        await bot.say("<@{}> Sing!".format(user.id))
    
@bot.command()
async def q(*args):
    await sayList()
    
@bot.command()
async def clear(*args):
    global userList
    global elected
    userList = []
    elected = 0
    await sayList()
    
@bot.command()
async def help(*args):
    description = ("\n")
    description += "join \n"
    description += "remove \n"
    description += "sing \n"
    description += "q \n"
    description += "clear \n"
        
    embed = discord.Embed(colour=0x0dbeff, description=description)  # Can use discord.Colour()
    embed.title = "Commands"
    
    await bot.say(embed=embed)

async def sayList():
    description = ("It's Friday!!!\n\n")
    #singer = None
    for i in range(len(userList)):
        user = userList[i]
        userLine = str(user.name)
        if i == elected:
            userLine = "**{}** :musical_note:".format(userLine)
    #        singer = user
        description += userLine + "\n"
        
    embed = discord.Embed(colour=0x0dbeff, description=description)  # Can use discord.Colour()
    embed.title = "Karaoke Singers"
    #embed.set_author(name="Karaoke")
    #if singer is not None:
    #    print(singer.avatar_url)
    #    embed.set_thumbnail(url=singer.avatar_url)
    embed.set_footer(text="\nCome! Join up!")

    await bot.say(embed=embed)
    

bot.run(os.environ.get('TOKEN'))
