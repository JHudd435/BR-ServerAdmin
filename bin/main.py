## This is the wrapper for br_bot and automod
import discord
from discord.ext import commands
from dotenv import load_dotenv
import subprocess
import os
import signal

# Init
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1247894755380297791  # Ensure this matches your Discord channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Store the process globally to allow stopping later
br_bot_process = None

# Ping up
@bot.event
async def on_ready():
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("BRSA Started.\nTo start BR-Bot, use !startbot on. To start automod, use !automod on. Use off instead of on to shut it off.")

# Commands
@bot.command(name='startbot', help="Starts up BR-Bot")
@commands.has_role('Bot Admin')
async def start_bot(ctx, *, state: str):
    global br_bot_process
    try:
        if state == "on":
            if br_bot_process is None:
                # Start BR-Bot as a subprocess
                br_bot_process = subprocess.Popen(['python', './bin/autmod.py'])
                await ctx.send("BR-Bot started.")
            else:
                await ctx.send("BR-Bot is already running.")
        elif state == "off":
            if br_bot_process is not None:
                # Terminate the BR-Bot subprocess
                br_bot_process.terminate()  # Gracefully terminate
                br_bot_process.wait()  # Wait for process to terminate
                br_bot_process = None
                await ctx.send("BR-Bot stopped.")
            else:
                await ctx.send("BR-Bot is not running.")
        else:
            await ctx.send("Invalid command. Use 'on' to start or 'off' to stop BR-Bot.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='automod', help="Starts up automod")
@commands.has_role('Bot Admin')
async def start_bot(ctx, *, state: str):
    global br_bot_process
    try:
        if state == "on":
            if br_bot_process is None:
                # Start AutoMod as a subprocess
                br_bot_process = subprocess.Popen(['python', './bin/automod.py'])
                await ctx.send("AutoMod started.")
            else:
                await ctx.send("AutoMod is already running.")
        elif state == "off":
            if br_bot_process is not None:
                # Terminate the AutoMod subprocess
                br_bot_process.terminate()  # Gracefully terminate
                br_bot_process.wait()  # Wait for process to terminate
                br_bot_process = None
                await ctx.send("AutoMod stopped.")
            else:
                await ctx.send("AutoMod is not running.")
        else:
            await ctx.send("Invalid command. Use 'on' to start or 'off' to stop AutoMod.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Run the bot
bot.run(TOKEN)
