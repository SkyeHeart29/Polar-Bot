# Installation Guide

* Install [Python 3.6.3](https://www.python.org/downloads/).
  * Open Powershell (Windows) or Terminal (OS X) and enter the following lines:
    * `pip install -U pip setuptools`
    * `pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]`
    * `pip install rethinkdb`
    * `pip install asyncio`
    * `pip install aiohttp`
    * `pip install beautifulsoup4`

* Install [RethinkDB](https://www.rethinkdb.com/).
  * [Start a RethinkDB server.](https://www.rethinkdb.com/docs/start-a-server/)
  * Leave the server online as the bot runs.
  
* Add a user bot.
  * Create an app [here](https://discordapp.com/developers/applications/me).
  * Once an app is created, copy the token under the Bot section.
  
* Starting the bot
  * Download the source code and paste it in your desired folder.
  * In Powershell/Terminal, change your current working directory to the desired folder. (Type `cd [PATH OF FOLDER]`)
  * Type `python bot.py [TOKEN]`, replacing [TOKEN] with the copied token.
  * The program will ask you which cog folder to load from. There are two folders in the root folder, `cogs` and `beta. Type `cogs` for Polar Bot's cogs or `beta` for Polar Bot Beta's cogs.
  * It would look something like this: ![Terminal](https://i.imgur.com/OJttfxq.png)
  
* Initialising the bot
  * Invite your bot to your server. Go [here](https://discordapi.com/permissions.html) to make an invite link.
  * At your server, type `.db create [X]` and replace X with the following (they are case-sensitive!):
    * bots
    * properties
    * tags
    * welcome
    * bots
    * help
  * Type `.db list` to ensure you have the required databases. (Ignore the database named `rethinkdb`)
  * Type `.bp create` to create a bot profile. You can edit the invite link, server link, etc. by reading the documentation for `bp` [here](https://github.com/polar-rex/Polar-Bot#bot-owner-only).
  * Type `.help create 0 [text]` to create the default help page.