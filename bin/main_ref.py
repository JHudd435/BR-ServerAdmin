import pyautogui
import re
import time
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import subprocess
import csv
from discord.ext import commands
from dotenv import load_dotenv
import time
import threading
import keyinputs
import schedule
import asyncio
import psutil

# Variables
load_dotenv()
pyautogui.FAILSAFE = False
pyautogui.FAILSAFE = False
lineList = []
bannedVehicles = []
lastLine = ""
base_dir = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL")
adminprefix = "admin_bot: "
Chat_key = "j"

files = {
    "strikes.csv": os.path.join(base_dir, "textfiles", "strikes.csv"),
    "banned_vehicles.txt": os.path.join(base_dir, "textfiles", "banned_vehicles.txt"),
    "players.csv": os.path.join(base_dir, "textfiles", "players.csv"),
}

for file_name, file_path in files.items():
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass
        print(f"Created missing file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

strikes_path = os.path.join(base_dir, "textfiles", "strikes.csv")
banned_path = os.path.join(base_dir, "textfiles", "banned_vehicles.txt")
playerdata_path = os.path.join(base_dir, "textfiles", "players.csv")

pyautogui.PAUSE = 0.3


# def focus():
#    win_activate(window_title="Brick Rigs", partial_match=True)
#    time.sleep(0.5)


# AutoMod Definitions
def readLogs():
    gameIni = open(
        f"/home/serverhost/.local/share/Steam/steamapps/compatdata/552100/pfx/drive_c/users/steamuser/AppData/Local/BrickRigs/SavedRemastered/Config/WindowsNoEditor/Game.ini",
        encoding="utf-8",
        mode="r",
    )
    lines = gameIni.readlines()
    gameIni.close()
    for line in lines:
        line = line.strip().rstrip()
        if "ChatMessageLog" in line:
            lineList.append(line)


def isopen():
    return "BrickRigs-Win64-Shipping.exe" in (i.name() for i in psutil.process_iter())


def load_csv_to_dict_strikes(file_path=strikes_path):
    players_dict = {}

    # Read the CSV and store data in a dictionary
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_id = row["playerid"]
            players_dict[player_id] = {
                "player": row["player"],
                "strike": int(
                    row["strike"]
                ),  # Convert strike to an integer for easier updating
            }
    return players_dict


import csv
import os


def add_player_to_log(playername, playerid, file_path=playerdata_path):
    # Check if file exists before reading
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["playerid"] == playerid:
                    print(f"Player ID {playerid} already exists. Skipping entry.")
                    return  # Exit function if player ID is already present

    # If the ID is not found, append it
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = ["player", "playerid"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if os.stat(file_path).st_size == 0:
            writer.writeheader()

        writer.writerow({"player": playername, "playerid": playerid})
        print(f"Added player {playername} with ID {playerid}.")


def overwrite_csv_with_dict(players_dict, file_path=strikes_path):
    # Open the CSV in write mode
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["player", "playerid", "strike"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header

        # Write each player's data back into the CSV
        for player_id, player_data in players_dict.items():
            writer.writerow(
                {
                    "player": player_data["player"],
                    "playerid": player_id,
                    "strike": player_data["strike"],
                }
            )
    print("CSV file updated successfully.")


def find_player_by_name(playername):
    with open(playerdata_path, mode="r", newline="", encoding="utf-8") as file:
        fieldnames = ["player", "playerid"]
        reader = csv.DictReader(file)
        for row in reader:
            if row["player"] == playername:
                return str(row["playerid"])


strikeCount = 0


def add_or_update_player(players_dict, player_name, player_id):
    # If the player_id exists, increment the strike count by 1, else add a new entry
    if player_id in players_dict:
        print(f"Incrementing strike count for player ID {player_id}")
        players_dict[player_id]["strike"] += 1  # Increment strike count by 1
    else:
        print(f"Adding new player {player_name} with ID {player_id}")
        players_dict[player_id] = {
            "player": player_name,
            "strike": 1,  # Initialize with a strike count of 1 for new players
        }


def get_strike_count(players_dict, player_id):
    # Check if the player_id exists in the dictionary
    if player_id in players_dict:
        return players_dict[player_id]["strike"]  # Return the strike count
    else:
        print(f"Player with ID {player_id} not found.")
        return None  # Return None if the player is not found


async def send_banned_vehicle_message(player_name, vehicle):
    channel = bot.get_channel(1301953975310090353)
    if channel:
        await channel.send(
            f"BANNED VEHICLE DETECTED! Player: {player_name}, Vehicle: {vehicle}."
        )


async def send_ban(player_name, player_id, vehicle):
    channel = bot.get_channel(1301953975310090353)
    if channel:
        await channel.send(
            f"---\nAutoMod: Banned {player_name} ({player_id}) for 1 minutes, spawned {vehicle}.\n---"
        )


async def send_jhudd():
    channel = bot.get_channel(1301953975310090353)
    if channel:
        await channel.send(
            f"---\nAutoMod: Jhudd spawned a banned vehicle, but as he is exempt from the rules that apply to mere mortals, there will be no consequences.\n---"
        )


async def send_message(message):
    channel = bot.get_channel(1301953975310090353)
    if channel:
        await channel.send(message)


async def send_permaban(player_name, player_id, vehicle):
    channel = bot.get_channel(1301953975310090353)
    if channel:
        await channel.send(
            f"---\nAutoMod: Permanently banned {player_name} ({player_id}) for getting more than 3 strikes, spawned {vehicle}\n---"
        )


async def hardrestart_sched():
    await keyinputs.sendmessage("AutoMod", "Server rebooting in 5 seconds.")
    await asyncio.sleep(5)
    await keyinputs.hardrestart()
    await send_message("Server hard restarted")
    await keyinputs.sendmessage("AutoMod", "Server successfully rebooted.")


def run_hardrestart_sched():
    loop = asyncio.get_event_loop()
    loop.create_task(hardrestart_sched())


async def warn(playerName, playerVehicle, strikeCount):
    # line one
    pyautogui.typewrite(Chat_key)
    time.sleep(0.05)
    pyautogui.typewrite(
        f"AutoMod:WARNING: {playerName} has spawned {playerVehicle}. Vehicle is banned."
    )
    time.sleep(0.05)
    pyautogui.press("enter")
    # line two
    time.sleep(0.1)
    pyautogui.typewrite(Chat_key)
    pyautogui.typewrite(
        f"Please delete vehicle, do not spawn it again. Failure to comply will result in a ban. Strikes: {strikeCount}/3"
    )
    time.sleep(0.05)
    pyautogui.press("enter")
    await send_banned_vehicle_message(playerName, playerVehicle)


async def kick(playerName, playerId, playerVehicle):
    # Ban
    time.sleep(1)
    pyautogui.press("esc")
    for i in range(3):
        pyautogui.press("tab")
        time.sleep(0.2)
    pyautogui.press("enter")
    for i in range(2):
        pyautogui.press("tab")
        time.sleep(0.2)
    pyautogui.press("enter")
    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.typewrite(str(playerId))
    pyautogui.press("enter")
    for i in range(5):
        pyautogui.press("tab")
        time.sleep(0.2)
    pyautogui.press("enter")
    pyautogui.typewrite(
        "AutoMod kicked you for spawning a banned vehicle. Read the rules."
    )
    pyautogui.press("enter")

    for i in range(4):
        pyautogui.press("tab")
        time.sleep(0.2)
    pyautogui.press("enter")
    pyautogui.typewrite("1")
    pyautogui.press("enter")
    for i in range(3):
        pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.press("esc")
    pyautogui.press("esc")
    await send_ban(playerName, playerId, playerVehicle)


import pyautogui


async def checkmatch():
    try:
        location = pyautogui.locateOnScreen("Orangewin.png", confidence=0.9)
        if location:
            screen_height = pyautogui.size().height
            image_bottom = location.top + location.height

            threshold = screen_height * 0.7

            if image_bottom >= threshold:
                print("Image found at the bottom, softrestarting")
                await keyinputs.softrestart()
                await send_message("Match restarted")
    except:
        return


# Create schedules
schedule.every().day.at("00:00").do(run_hardrestart_sched)
schedule.every().day.at("04:00").do(run_hardrestart_sched)
schedule.every().day.at("08:00").do(run_hardrestart_sched)
schedule.every().day.at("12:00").do(run_hardrestart_sched)
schedule.every().day.at("16:00").do(run_hardrestart_sched)
schedule.every().day.at("20:00").do(run_hardrestart_sched)

# Init general
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Init automod
banned = open(banned_path, encoding="utf-8", mode="r")
bannedlines = banned.readlines()
banned.close()
for line in bannedlines:
    line = line.strip().rstrip()
    bannedVehicles.append(line)

players_dict = load_csv_to_dict_strikes()
patternType = re.compile(r"Type=(?P<Type>\w+),")
patternSpawn = re.compile(
    r"Type=(?P<Type>\w+),"
    r'Player=\(PlayerId=(?P<PlayerId>\d+),PlayerName="(?P<PlayerName>[^"]+)"\),'
    r'.*TextOption=INVTEXT\("(?P<TextOption>.*)"\)'  # Modified to capture all text inside INVTEXT
)
patternJoin = re.compile(
    r'Player=\(PlayerId=(?P<PlayerId>\d+),PlayerName="(?P<PlayerName>[^"]+)"\)'
)


# BRBOT
## Commands


# Send a message as admin
@bot.command(name="msg", help="Sends a message as an admin")
@commands.has_role("Bot Admin")
async def msg(ctx, *, message: str):

    try:
        messenger = ctx.author.name
        await keyinputs.sendmessage(messenger, message)
        await ctx.send("Message sent!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Reboot the match
@bot.command(name="softrestart", help="Restarts the match")
@commands.has_role("Bot Admin")
async def softrestart(ctx):

    await keyinputs.softrestart()
    await ctx.send("Server has been soft rebooted")


# Weather command
@bot.command(
    name="weather",
    help="Changes the weather. Can be changed to sunny, partcloudy, cloudy, highfog, sunnywet, sunnysnow, rain, thunder, snow",
)
@commands.has_role("Bot Admin")
async def weather(ctx, *, weather: str):

    weather_response = await keyinputs.setweather(
        weather
    )  # OMG NO WAY!!! So nice and clean!!!!!
    if weather_response == "Invalid_Weather":
        await ctx.send("Invalid weather.")
        return
    else:
        await ctx.send("Weather changed")


# Ban Command
@bot.command(name="banid", help="Bans a user by their steam64 ID")
@commands.has_role("Bot Admin")
async def banid(ctx, id: str, length: str = "10", *, reason: str = None):

    guild = ctx.guild
    if id != "76561199656519803":
        ban_response = await keyinputs.banid(id, length, reason)
        await ctx.send(ban_response)
    else:
        await ctx.send(
            ctx.author.mention
            + " You attempted to ban Jhudd the Magnificent, the Immortal, the Incredible. Refrain from doing so. "
        )


@bot.command(name="ban", help="Bans a user by their name")
@commands.has_role("Bot Admin")
async def ban(ctx, id: str, length: str = "10", *, reason: str = None):

    guild = ctx.guild
    idname = find_player_by_name(id)
    if idname =="76561199656519803":
        await ctx.send(
            ctx.author.mention
            + " You attempted to ban Jhudd the Magnificent, the Immortal, the Incredible. Refrain from doing so. "
        )
        
    elif idname != None:
        ban_response = await keyinputs.banid(idname, length, reason)
        await ctx.send(ban_response)
    else:
        await ctx.send("Could not find player name.")


# Unban command
@bot.command(name="unban", help="Unbans a user by their steam64 ID")
@commands.has_role("Bot Admin")

async def unban(ctx, id: str):
    if not id.isdigit():
        try:
            id = await asyncio.to_thread(find_player_by_name, id)
            if not id:
                await ctx.send("Player not found.")
                return
        except Exception as e:
            print(f"Error finding player: {e}")
            await ctx.send("Could not resolve player name.")
            return

    try:
        await keyinputs.unban(id)
        await ctx.send(f"{id} unbanned")
    except Exception as e:
        print(f"Error unbanning: {e}")
        await ctx.send("Failed to unban player.")


# Hard restart command
@bot.command(name="hardrestart", help="Kills the server and then starts it again")
@commands.has_role("Bot Admin")
async def hardrestart(ctx):
    await ctx.send("Restarting server...")
    await keyinputs.hardrestart()
    await ctx.send("Server has been hard rebooted")


# Set the time
@bot.command(name="settime", help="Sets the time in 24 hr whole number format")
@commands.has_role("Bot Admin")
async def settime(ctx, timesetting: str):
    pyautogui.press("esc")
    time.sleep(0.1)
    for i in range(4):
        pyautogui.press("tab")
        time.sleep(0.1)
    pyautogui.press("enter")
    for i in range(28):
        pyautogui.press("tab")
        time.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.typewrite(timesetting)
    pyautogui.press("enter")
    pyautogui.press("esc")
    time.sleep(0.1)
    pyautogui.press("esc")
    await ctx.send(f"Time changed to {timesetting}.")


# Get online players
@bot.command(name="online", help="Gets online players")
@commands.has_role("Bot Admin")
async def online(ctx):

    pyautogui.press("capslock")
    time.sleep(1.5)
    players_online = pyautogui.screenshot()
    players_online.save("players.png")
    pyautogui.press("capslock")
    await ctx.send(file=discord.File("players.png"))


# Screenshot
@bot.command(name="screen", help="Screenshots")
@commands.has_role("Bot Admin")
async def online(ctx):
    guild = ctx.guild
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screen.png")
        await ctx.send(file=discord.File("screen.png"))
    except Exception as e:
        await ctx.send(e)


# Die
autokill = False


@bot.command(name="die", aliases=["kys"], help="Kills admin")
@commands.has_role("Bot Admin")
async def die(ctx):
    global autokill
    if autokill == True:
        autokill = False
        await ctx.send("Toggled autokill to `False`")
    elif autokill == False:
        autokill = True
        await ctx.send("Toggled autokill to `True`")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


counter = 0


# AUTOMOD
@tasks.loop(seconds=0.5)
async def monitor_logs():
    global lastLine  # Allow modification of the global lastLine variable
    global counter
    await checkmatch()
    schedule.run_pending()

    try:
        readLogs()
    except Exception as e:
        print(f"Error reading logs: {e}")
        return
    if autokill == True:
        if counter >= 30:
            pyautogui.press("end")
            counter = 0
        else:
            counter = counter + 1
    else:
        pass
    if (
        lineList and str(lineList[-1]) != lastLine
    ):  # Check if lineList has data and compare to lastLine
        matchType = patternType.search(str(lineList[-1]))
        if matchType:
            logDataType = matchType.groupdict()

            if logDataType["Type"] == "VehicleSpawnSuccess":
                match = patternSpawn.search(str(lineList[-1]))
                if match:
                    logData = match.groupdict()
                    playerName = logData["PlayerName"]
                    playerVehicle = logData["TextOption"]
                    playerId = logData["PlayerId"]

                    print(
                        f"Spawn Attempt: Player Name: {playerName}, Vehicle: {playerVehicle}"
                    )
                    lastLine = str(
                        lineList[-1]
                    )  # Update lastLine after processing the current line

                    if any(
                        banned_vehicle.lower() in playerVehicle.lower()
                        for banned_vehicle in bannedVehicles
                    ):
                        if playerId != "76561199656519803":
                            # tab these lines
                            print("WARNING! BANNED VEHICLE DETECTED!")
                            add_or_update_player(players_dict, playerName, playerId)
                            await kick(playerName, playerId, playerVehicle)
                            overwrite_csv_with_dict(players_dict)
                        else:
                            await send_jhudd()

            elif logDataType["Type"] == "Join":
                match = patternJoin.search(str(lineList[-1]))
                if match:
                    logData = match.groupdict()
                    playerName = logData["PlayerName"]
                    playerId = logData["PlayerId"]
                    lastLine = str(lineList[-1])
                    add_player_to_log(playerName, playerId)
                    await send_message(
                        f"---\nJOIN:\nName: {playerName}\nID: {playerId}\n---"
                    )


# End boilerplate
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("BRSA 1.0 2025 by Jhudd073, Anti")
    await channel.send("Automod On")
    await channel.send("BrBot On")
    monitor_logs.start()


bot.run(TOKEN)
