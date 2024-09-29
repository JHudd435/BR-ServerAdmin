import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pyautogui
import time
import signal
import sys
import imports
import subprocess


#Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
adminprefix = "admin_bot: "
pyautogui.FAILSAFE = False

# Define signal handler for graceful shutdown
def handle_termination(signum, frame):
    print("BR-BOT received termination signal.")
    sys.exit(0)

# Register the signal handler for termination (SIGTERM)
signal.signal(signal.SIGTERM, handle_termination)

# Ping up
@bot.event
async def on_ready():
    channel = bot.get_channel(int(CHANNEL))
    await channel.send("BR-BOT 2024, Jhudd073. Bot is now online.")

# Vars

#Defs

def weatherinit():
        pyautogui.press('esc')
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        for i in range(35):
            pyautogui.press('tab')
            time.sleep(0.1)



#Commands

# Send a message as admin
@bot.command(name='adminmessage',help="Sends a message as an admin")
@commands.has_role('Bot Admin')
async def adminmessage(ctx, *, message: str):
    try:
        pyautogui.typewrite('j')
        pyautogui.typewrite(f'{ctx.author.name}@Discord: {message}')
        time.sleep(0.05)
        pyautogui.press('enter')

        await ctx.send("Message sent!")
        time.sleep(0.05)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Reboot the match
@bot.command(name='softrestart', help="Restarts the match")
@commands.has_role('Bot Admin')
async def adminmessage(ctx):
    pyautogui.press('esc')
    for i in range(4):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    await ctx.send("Server has been soft rebooted")


# Weather command
@bot.command(name='weather',help="Changes the weather. Can be changed to sunny, partcloudy, cloudy, highfog, sunnywet, sunnysnow, rain, thunder, snow")
@commands.has_role('Bot Admin')
async def weather(ctx, *, weather:str):
            
    # paths
    if(weather=="sunny"):
        weatherinit()
        pyautogui.press('tab')
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="partcloudy"):
        weatherinit()
        for i in range(2):
            pyautogui.press('tab')
            time.sleep(0.03)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="cloudy"):
        weatherinit()
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="highfog"):
        weatherinit()
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="sunnywet"):
        weatherinit()
        for i in range(5):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="sunnysnow"):
        weatherinit()
        for i in range(6):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="rain"):
        weatherinit()
        for i in range(7):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="thunder"):
        weatherinit()
        for i in range(8):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)

    elif(weather=="snow"):
        weatherinit()
        for i in range(9):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press('esc')
            time.sleep(0.1)
    else:
        await ctx.send("Invalid weather.")
    await ctx.send("Weather changed")
    



# ban command
@bot.command(name='banid', help="Bans a user by their steam64 ID")
@commands.has_role('Bot Admin')
async def banid(ctx, id: str, length:str, reason:str="Default Reason."):
    guild = ctx.guild
    user = imports.getSteamUser(id)
    username = user['player']['personaname']
    pyautogui.press('esc')
    for i in range(3):
        pyautogui.press('tab')
        time.sleep(0.1)    
    pyautogui.press('enter')
    for i in range(2):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter') 
    pyautogui.typewrite(str(id))
    pyautogui.press('enter')
    for i in range(5):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.typewrite(f"You have been banned by a Discord admin for reason: {reason}. You may appeal this ban in the Discord.")
    pyautogui.press('enter')
    if(length=='10'):
        for i in range(7):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        pyautogui.press('esc')
        pyautogui.press('esc')
        await ctx.send(f"{id} AKA {username} banned for 10 minutes, reason {reason}")
    elif(length=='inf'):
        for i in range(6):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        pyautogui.press('tab')
        pyautogui.press('enter')
        pyautogui.press('esc')
        pyautogui.press('esc')
        await ctx.send(f"{id} AKA {username} banned for infinity, reason {reason}")
    else:
        await ctx.send("At this time, banning someone for a time other than 10 or inf is not supported.")

# hard reboot command
def killbr():
    subprocess.call("TASKKILL /F /IM BrickRigs-Win64-Shipping.exe")

def startbr():
    os.startfile("steam://rungameid/552100")

@bot.command(name='hardrestart', help="Kills the server and then starts it again")
@commands.has_role('Bot Admin')
async def hardrestart(ctx):
    guild = ctx.guild
    await ctx.send("Restarting server...")
    killbr()
    time.sleep(5)
    startbr()
    time.sleep(25)
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    await ctx.send("Server has been hard rebooted")

# Set the time
@bot.command(name='settime', help="Sets the time in 24 hr whole number format")
@commands.has_role('Bot Admin')
async def settime(ctx, timesetting:str):
    guild = ctx.guild
    pyautogui.press('esc')
    time.sleep(0.1)
    for i in range(4):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press('enter')
    for i in range(28):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.typewrite(timesetting)
    pyautogui.press('enter')
    pyautogui.press('esc')
    time.sleep(0.1)
    pyautogui.press('esc')
    await ctx.send(f"Time changed to {timesetting}.")



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)