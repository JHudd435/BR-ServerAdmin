**BR_BOT Manual**
*1.*
`!msg`: 
Sends a message to the server as admin. Use to warn people or just send a more official message.
Arguments: `!msg message`
Example: `!msg Tonald_Dump, please delete the garie.`

*2.*
`!softrestart`: 
Restarts the match. This can be used if the server is getting laggy, or if a team wins and the server goes to the proceed screen. The bot should be able to auto restart the server on match end soon, though.
Example: `!softrestart`

*3.*
`!weather`: 
Changes the weather. It can be set to `sunny, partcloudy, cloudy, highfog, sunnywet, sunnysnow, rain, thunder, snow`. Use this sparingly.
Arguments: `!weather weather`
Example: `!weather sunnywet`

*4.*
`!banid`: 
The most important command of the bot, this will ban the given user. It has two modes, `inf` and `10`, which permaban and 10 minute ban, respectively. To get the id, paste the user's profile into https://steamid.uk/.
Arguments: `!banid id length reason`
Example: `!banid 76561198121823989 10 Teamkilling, op vehicle.`

*5.*
`!unban`: 
For when you ban someone by mistake, or they successfully appeal their ban. 
Arguments: `!unban id`
Example: `!unban 76561198121823989`

*6.*
`!hardrestart`: 
For when the server crashes or because it's no longer visible. Just be aware, just because you can't see it doesn't mean people are not on the server. Use `!online` to verify the server is empty or crashed.
Example: `!hardrestart`

*7.*
`!settime`: 
Sets the time, using 24/hr time in whole numbers. It does support decimals, but please avoid using them. 24 hour time means that 0=Midnight, 12=Noon.
Example: `!settime 14`

*8.*
`!online`: 
Screenshots the player list and sends it to the channel.
Example: `!online`

*9.*
`!screen`: 
Screenshots the server and sends it to the channel. Use to determine if the bot is stuck somewhere, as this command will work unless the host pc is crashed. If the bot is in a menu, try using `!softrestart` to get it back to it's normal state, which should just be the normal play screen. If this fails, a `!hardrestart` may be neccessary.
If this returns `Brick Rigs is not foreground`, this means that the server for some reason or another is not maximized. Could be a crash, could be a popup, could be anything. A `!hardrestart` is absolutely neccessary at this point.
Example: `!screen`

*10. (Not implemented)*
`!chat`: 
Screenshots  the chat and sends it to the server. In the future, this will have it's own channel with an automatically updating image. Use this to be nosy or to see if anyone is saying something they shouldn't.
Example: `!chat`

*11. (Not implemented)*
`!die`: 
Assassinates the host. In the future, this will be done automatically every 10 seconds. Use this if the host is the only one left alive or if the host forgot to turn the bot off when he got online.
Example: `!die`
