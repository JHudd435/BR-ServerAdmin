import pyautogui
import re
import time
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import csv

time.sleep(2)
pyautogui.FAILSAFE = False
lineList = []
bannedVehicles = []
lastLine = ""  # Declare lastLine globally so it persists between loop iterations

# init
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL')  # Ensure this matches your Discord channel ID

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

csvpath = "./textfiles/strikes.csv"
winUser = os.getlogin()


# Load banned vehicles
banned = open("./textfiles/banned_vehicles.txt", encoding="utf-8", mode="r")
bannedlines = banned.readlines()
banned.close()
for line in bannedlines:
    line = line.strip().rstrip()
    bannedVehicles.append(line)

print(bannedVehicles)

def readLogs():
    gameIni = open(f"C:/Users/{winUser}/AppData/Local/BrickRigs/SavedRemastered/Config/WindowsNoEditor/game.ini", encoding="utf-8", mode="r")
    lines = gameIni.readlines()
    gameIni.close()
    for line in lines:
        line = line.strip().rstrip()
        if "ChatMessageLog" in line:
            lineList.append(line)

#CSV handling:

import csv

# 1. Function to pull the CSV into a dictionary
def load_csv_to_dict(file_path=csvpath):
    players_dict = {}
    
    # Read the CSV and store data in a dictionary
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_id = row['playerid']
            players_dict[player_id] = {
                'player': row['player'],
                'strike': int(row['strike'])  # Convert strike to an integer for easier updating
            }
    return players_dict

# 2. Function to add or update entries in the dictionary and increment the strike count
def add_or_update_player(players_dict, player_name, player_id):
    # If the player_id exists, increment the strike count by 1, else add a new entry
    if player_id in players_dict:
        print(f"Incrementing strike count for player ID {player_id}")
        players_dict[player_id]['strike'] += 1  # Increment strike count by 1
    else:
        print(f"Adding new player {player_name} with ID {player_id}")
        players_dict[player_id] = {
            'player': player_name,
            'strike': 1  # Initialize with a strike count of 1 for new players
        }

# 3. Function to overwrite the CSV with the updated dictionary
def overwrite_csv_with_dict(players_dict, file_path=csvpath):
    # Open the CSV in write mode
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['player', 'playerid', 'strike']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header
        
        # Write each player's data back into the CSV
        for player_id, player_data in players_dict.items():
            writer.writerow({
                'player': player_data['player'],
                'playerid': player_id,
                'strike': player_data['strike']
            })
    print("CSV file updated successfully.")


def get_strike_count(players_dict, player_id):
    # Check if the player_id exists in the dictionary
    if player_id in players_dict:
        return players_dict[player_id]['strike']  # Return the strike count
    else:
        print(f"Player with ID {player_id} not found.")
        return None  # Return None if the player is not found

players_dict = load_csv_to_dict()

# Example usage
# Load the CSV into a dictionary
players_dict = load_csv_to_dict()




# Check type
patternType = re.compile(r"Type=(?P<Type>\w+),")
patternSpawn = re.compile(
    r'Type=(?P<Type>\w+),'
    r'Player=\(PlayerId=(?P<PlayerId>\d+),PlayerName="(?P<PlayerName>[^"]+)"\),'
    r'.*TextOption=INVTEXT\("(?P<TextOption>.*)"\)'  # Modified to capture all text inside INVTEXT
)

# Function to send a message to the Discord channel
async def send_banned_vehicle_message(player_name, vehicle):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"BANNED VEHICLE DETECTED! Player: {player_name}, Vehicle: {vehicle}")

async def send_ban(player_name, player_id, vehicle):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"AutoMod: Banned {player_name} ({player_id}) for spawning {vehicle}")

# Task to monitor the game logs
@tasks.loop(seconds=2)
async def monitor_logs():
    global lastLine  # Allow modification of the global lastLine variable
    try:
        readLogs()
    except Exception as e:
        print(f"Error reading logs: {e}")
        return

    if lineList and str(lineList[-1]) != lastLine:  # Check if lineList has data and compare to lastLine
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

                    print(f"Spawn Attempt: Player Name: {playerName}, Vehicle: {playerVehicle}")
                    lastLine = str(lineList[-1])  # Update lastLine after processing the current line

                    if any(banned_vehicle.lower() in playerVehicle.lower() for banned_vehicle in bannedVehicles):
                        print("WARNING! BANNED VEHICLE DETECTED!")
                        add_or_update_player(players_dict,playerName,playerId)
                        strikeCount = get_strike_count(players_dict,playerId)
                        if (strikeCount <3):
                            #line one
                            pyautogui.typewrite('j')
                            pyautogui.typewrite(f'AutoMod:WARNING: {playerName} has spawned {playerVehicle}. Vehicle is banned.')
                            time.sleep(0.05)
                            pyautogui.press('enter')
                            #line two
                            time.sleep(0.1)
                            pyautogui.typewrite('j')
                            pyautogui.typewrite(f'Please delete vehicle, do not spawn it again. Failure to comply will result in a ban. Strikes: {strikeCount}/3')
                            time.sleep(0.05)
                            pyautogui.press('enter')
                            await send_banned_vehicle_message(playerName, playerVehicle)
                        else:
                            # Ban
                            time.sleep(1)
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
                            pyautogui.typewrite(str(playerId))
                            pyautogui.press('enter')
                            for i in range(5):
                                pyautogui.press('tab')
                                time.sleep(0.1)
                            pyautogui.press('enter')
                            pyautogui.typewrite("AutoMod kicked you for spawning a banned vehicle. If you continue to spawn banned vehicles in the future, you will be permabanned.")
                            pyautogui.press('enter')

                            for i in range(7):
                                pyautogui.press('tab')
                                time.sleep(0.1)
                            pyautogui.press('enter')
                            pyautogui.press('esc')
                            pyautogui.press('esc')
                            await send_ban(playerName,playerId,playerVehicle)
                            

                        overwrite_csv_with_dict(players_dict)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("AutoMod 1.0 2024, Jhudd073. AutoMod is now online.")
    monitor_logs.start()

# Start the bot
client.run(TOKEN)

