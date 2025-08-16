import os
import csv

base_dir = os.path.dirname(os.path.abspath(__file__))

playerdata_path = os.path.join(base_dir, "textfiles", "players.csv")


def find_player_by_name(playername):
    with open(playerdata_path, mode="r", newline="", encoding="utf-8") as file:
        fieldnames = ["player", "playerid"]
        reader = csv.DictReader(file)
        for row in reader:
            if row["player"] == playername:
                return str(row["playerid"])


player1 = find_player_by_name("Anti")

print(player1)
