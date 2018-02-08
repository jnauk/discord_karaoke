import discord
from discord.ext.commands import Bot
from discord.ext import  commands
import asyncio
import time
import os
from datetime import date
import calendar

PREFIX = "-"

Client = discord.Client()
bot = commands.Bot(command_prefix=PREFIX, pm_help = False)
bot.remove_command("help")

userListPerServer = {}

@bot.event
async def on_ready():
    print("Bot is ready!")
    
@bot.command(pass_context=True)
async def join(ctx):
    user = ctx.message.author
    userList = getServerList(ctx.message.server.id)
    if user not in userList:
        userList.append(user)    
    await sayList(userList)

@bot.command(pass_context=True)
async def leave(ctx):
    user = ctx.message.author
    userList = getServerList(ctx.message.server.id)
    userList.remove(user)    
    await sayList(userList)

@bot.command(pass_context=True)
async def q(ctx):
    userList = getServerList(ctx.message.server.id)
    await sayList(userList)

@bot.command(pass_context=True)
async def sing(ctx):
    if await isAdmin(ctx.message.author):
        userList = getServerList(ctx.message.server.id)
        if len(userList) > 0:
            userToJump = None
            args = ctx.message.content.split(" ")
            if len(args) == 2:
                userIndex = int(args[1])-1
                singJump(userList, userIndex)
            else:
                singNext(userList)
                
        await sayList(userList)
        if len(userList) > 0:
            userOnTop = userList[0]
            await bot.say("<@{}> Sing!".format(userOnTop.id))
            
@bot.command(pass_context=True)
async def remove(ctx):
    if await isAdmin(ctx.message.author):
        userList = getServerList(ctx.message.server.id)
        args = ctx.message.content.split(" ")
        userIndex = int(args[1])-1
        if userIndex >= 0 and userIndex < len(userList):
            userList.pop(userIndex)
        await sayList(userList)
    
@bot.command(pass_context=True)
async def clear(ctx):
    if await isAdmin(ctx.message.author):
        userList = getServerList(ctx.message.server.id)
        userList.clear()
        await sayList(userList)

@bot.command()
async def help(*args):
    description = ("\n")
    description += "**{}join** - Join the queue \n".format(PREFIX)
    description += "**{}leave** - Leave the queue \n".format(PREFIX)
    description += "**{}q** - Show the queue \n".format(PREFIX)
    
    description += "**{}sing** - Admin command. Next singer in line or singer by position \n".format(PREFIX)
    description += "**{}remove** - Admin command. Remove a singer by position \n".format(PREFIX)
    description += "**{}clear** - Admin command. Clear the queue \n".format(PREFIX)
        
    embed = discord.Embed(colour=0x0dbeff, description=description)  # Can use discord.Colour()
    embed.title = "Commands"
    
    await bot.say(embed=embed)

def getServerList(serverId):
    userList = None
    if serverId in userListPerServer:
        userList = userListPerServer[serverId]
    else:
        userList = []
        userListPerServer[serverId] = userList
    return userList

async def isAdmin(author):
    if author.server_permissions.administrator:
        return True
    elif "DJ" in [role.name for role in author.roles]:
        return True
    else:
        await bot.say("call an admin!")
        return False

async def sayList(userList):
    actualDate = date.today()
    dayOfWeek = calendar.day_name[actualDate.weekday()]
    description = "It's {}!!!\n\n".format(dayOfWeek)
    singer = None
    for i in range(len(userList)):
        user = userList[i]
        userLine = user.nick
        if userLine == None:
            userLine = user.name
        userLine = str(userLine)
        if i == 0:
            userLine = "**{}** :musical_note:".format(userLine)
            singer = user
        description += "`{}.` {}\n".format(i+1, userLine)
        
    embed = discord.Embed(colour=0x0dbeff, description=description)  # Can use discord.Colour()
    embed.title = "Karaoke Singers"
    #embed.set_author(name="Karaoke")
    if singer is not None:
    #    print(singer.avatar_url)
        embed.set_thumbnail(url=singer.avatar_url)
    embed.set_footer(text="\nCome! Join up!")

    await bot.say(embed=embed)
     
def singNext(userList):
    userOnTop = userList.pop(0)
    userList.append(userOnTop) 
    
def singJump(userList, userIndex):
    if userIndex > 0 and userIndex < len(userList):
        userToJump = userList.pop(userIndex)
        userOnTop = userList.pop(0)
        userList.append(userOnTop)        
        userList.insert(0, userToJump)
    
#bot.run(os.environ.get('TOKEN'))
bot.run("NDA5MDEzOTcyNDc0NTI3NzQ1.DVYcEQ.AOPcoSPZpsW7k4bpSpU-fHXwn_8")
