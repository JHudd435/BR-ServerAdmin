# BR-ServerAdmin
Administrative system for the game brick rigs

# Install
First, follow this guide until the end of the "Creating an Application" section.

Download the release or source from this github.

Creat a file called .env inside the bin folder. Inside of it, paste this:

```
# .env
DISCORD_TOKEN="Your_token_here"
CHANNEL="Your_channel_id"

```

Inside the quotation marks, paste your discord token and the channel id of the channel you want the bot to send messages to. To do this, you need to enable dev options in discord, right click the channel, and click "Copy Channel Id"

Next, if you want to use automod, open `banned_vehicles.txt` inside of the `textfiles` folder. Here you can paste vehicles you want to be banned.

Install the packages in requirements.txt

Add a "Bot Admin" role, exact spelling, in your discord server. Users must have this role to use the bot.

Installation is complete.

# Usage
Run main.py. If install was successful, you should get a message in the channel you have configured. To activate br-bot, which is controlled by bot admins to administrate the brick rigs server, use `!startbot on`.

To activate automod, which automatically warns and then bans users who spawn vehicles in the banlist, use `!automod on`. To switch either off, use `!startbot off` or `!automod off`.

## Br-Bot commands
`!banid id length reason` : This command will ban the user of the corresponding steamid. id: steamid. length: use either 10 or inf. reason: Put your reason in quotes "You suck lol". This can be left empty for default message.

`!adminmessage message` : This command will send a message thru brick rigs.

`!softrestart` : This will restart the match.

`!weather weather ` : Sets the weather. Use `sunny, partcloudy, cloudy, highfog, sunnywet, sunnysnow, rain, thunder, or snow`.

`!hardrestart` : Kills the server and starts it again. Useful if the server is crashed.

`!settime time`: Sets the time. Use whole numbers, 24 hr time. As is 12, 24, 10. Not as in 12:30, 1:30, etc.
