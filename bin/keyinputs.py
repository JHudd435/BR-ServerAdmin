import pyautogui
import time
import os
import subprocess
import psutil
import asyncio

Chat_key = "j"


async def sendmessage(messenger, message):
    pyautogui.typewrite(Chat_key)
    time.sleep(0.5)
    pyautogui.typewrite(f"{messenger}: {message}")
    time.sleep(0.05)
    pyautogui.press("enter")


async def softrestart():
    pyautogui.press("esc")
    for i in range(4):
        pyautogui.press("tab")
        time.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.press("enter")


def killbr():
    target = "BrickRigs-Win64-Shipping.exe".lower()

    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmdline = proc.info["cmdline"]
            if not cmdline:
                continue
            joined_cmdline = " ".join(cmdline).lower()
            if target in joined_cmdline:
                print(f"Killing PID {proc.pid}: {joined_cmdline}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError) as e:
            continue


def startbr():
    subprocess.run(["steam", f"steam://run/552100"])


async def hardrestart():
    killbr()
    await asyncio.sleep(5)
    startbr()
    await asyncio.sleep(40)
    pyautogui.press("enter")
    await asyncio.sleep(3)
    pyautogui.press("tab")
    await asyncio.sleep(3)
    pyautogui.press("enter")


async def setweather(weather):
    if weather not in (
        "sunny",
        "partcloudy",
        "cloudy",
        "highfog",
        "sunnywet",
        "sunnysnow",
        "rain",
        "thunder",
        "snow",
    ):
        return "Invalid_Weather"

    # Initialize
    pyautogui.press("esc")
    for i in range(4):
        pyautogui.press("tab")
        time.sleep(0.1)
    pyautogui.press("enter")
    for i in range(35):
        pyautogui.press("tab")
        time.sleep(0.1)

    # paths
    if weather == "sunny":
        pyautogui.press("tab")
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "partcloudy":
        for i in range(2):
            pyautogui.press("tab")
            time.sleep(0.03)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "cloudy":
        for i in range(3):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "highfog":
        for i in range(4):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "sunnywet":
        for i in range(5):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "sunnysnow":
        for i in range(6):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "rain":
        for i in range(7):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "thunder":
        for i in range(8):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)
    elif weather == "snow":
        for i in range(9):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        time.sleep(0.5)
        for i in range(2):
            pyautogui.press("esc")
            time.sleep(0.1)

    else:
        return "Invalid_Weather"

reasons={
    "1":"Lag.",
    "2":"OP vehicle.",
    "3":"Armed UV.",
    "4":"Hypermanuverable.",
    "5":"Stacked cannon/launcher",
    "6":"Racism/Slurs",
    "7":"Spawnkill",
    "8":"Stalling",
    "9":"Grave spotting",
    "10":"General reason."
}
def getreason(reasonnum):
    return reasons.get(reasonnum,None)

async def banid(id, length, reason):
    if getreason(reason) != None:
        reason = "Bot Ban: " + getreason(reason)

        if length not in ("10", "inf"):
            return "At this time, banning someone for a time other than 10 or inf is not supported."

        pyautogui.press("esc")
        for i in range(3):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        for i in range(2):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.typewrite(str(id))
        pyautogui.press("enter")
        for i in range(5):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.press("enter")
        pyautogui.typewrite(reason)
        pyautogui.press("enter")

        if length == "10":
            for i in range(7):
                pyautogui.press("tab")
                time.sleep(0.1)
            pyautogui.press("enter")
            pyautogui.press("esc")
            pyautogui.press("esc")
            return f"{id} banned for 10 minutes, reason {reason}"
        elif length == "inf":
            for i in range(6):
                pyautogui.press("tab")
                time.sleep(0.1)
            pyautogui.press("enter")
            pyautogui.press("tab")
            pyautogui.press("enter")
            pyautogui.press("esc")
            pyautogui.press("esc")
            return f"{id} banned for infinity, reason {reason}"
        else:
            return "At this time, banning someone for a time other than 10 or inf is not supported."
    else:
        return "Please use a number from the selection. Use !help banid or !help ban for more info."


async def settime(timesetting):
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


async def unban(id):
    pyautogui.press("esc")
    for i in range(3):
        pyautogui.press("tab")
        time.sleep(0.1)
    pyautogui.press("enter")
    time.sleep(1)
    for i in range(3):
        pyautogui.press("right")
        time.sleep(0.5)
    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.typewrite(str(id))
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("left")
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.press("left")
    for i in range(3):
        pyautogui.press("down")
        time.sleep(0.05)
    pyautogui.press("enter")
    time.sleep(1.5)
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.press("esc")
    time.sleep(0.1)
    pyautogui.press("esc")


"""AUTOMOD FUNCTION"""
