# Polar Bot
A polar bear Discord bot that stores tags, plays music, perform moderation functions and many other things. [**Invite Polar Bot to your server now***!](https://discordapp.com/oauth2/authorize?client_id=294708056112234497&scope=bot&permissions=406121544&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Fpolar-rex%2FPolar-Bot)

**Untick Administrator if you don't plan on using the moderation commands.*

## Notes
* To use a command, prefix with a full stop/period. You can change the prefix via the `prefix` command. Ping the bot to check what prefix is used for your server.
* Have any questions or problems regarding Polar Bot? Join [**The Arctic Den**](https://discord.gg/invite/5cxuTyN)! You'll also get a chance to try out the beta version of the bot.
* If you want to use my bot, check out the [installation guide](https://github.com/polar-rex/Polar-Bot/blob/master/installation.md).

## Commands
* `[]` is a mandatory argument while `()` is an optional argument.

### General
* `connections` - Shows the number of servers the bot is in.
* `help (command)` - Shows the help page.
* `invite` - Shows the invite link for Polar Bot.
* `ping` - Pong!
* `prefix [prefix]` - Changes the command prefix used for the bot server-wide. Caller requires *manage server* permission.
* `server` - Shows the invite link for The Arctic Den server.

### Moderation
* `ban [member]` - Bans a member. Caller requires *ban members* permission.
* `clear [number]` - Clears a number of recent messages from a channel. Caller requires *manage messages* permission.
* `kick [member]` - Kicks a member. Caller requires *kick members* permission.

### Recreational
* `me [message]` - An adoption of Skype's /me command.

### Memory
* **Tag** (See [*Tag Format Objects*](https://github.com/polar-rex/Polar-Bot#tag-formatting). Aliases: `tag`, `t`)
  * `t [tag] (arg1) (arg2)` - Returns the content of the tag.
  * `t create [tag] [message] (arg1) (arg2)` - Creates a tag. `@here` or `@everyone` cannot be used in a tag.
  * `t delete [tag]` - Deletes a tag if you're the owner.
  * `t list (member)` - Returns a list of the member's tags. If no member is given, then the caller's tags are returned.
* **Welcome** (See [*Welcome Format Objects*](https://github.com/polar-rex/Polar-Bot#tag-format-objects). Caller requires *manage server* permission)
  * `welcome here` - Changes which channel the welcome message will be posted to the channel the caller is in. 
  * `welcome message [message]` - Sets the welcome message.
  * `welcome mode` - Sends the welcome message via DM to the new user or a text channel.
  * `welcome toggle` - Turns on or off the welcome functionality.

### Search
* `yt [search]` - Returns a YouTube link. (Alias: `youtube`)

### Voice (Disabled until further notice)
* `forceskip` - Force-skips current song. Caller requires  *deafen members* permission.
* `pause` - Pauses current song. Caller requires *deafen members* permission.
* `play [url/title]` - Plays a song. [Supported URLs](https://rg3.github.io/youtube-dl/supportedsites.html).
* `playlist` - Shows the current queue.
* `resume` - Resumes a paused song. Caller requires *deafen members* permission.
* `skip` - Skips current song.
* `stop` - Stops the audio and makes the bot leave the voice channel. Caller requires *deafen members* permission.
* `summon` - Makes the bot join the voice channel the caller is in.
* `volume [1-100]` - Set the volume of current song. Caller requires *deafen members* permission.

### Bot Owner Only
* `extensions` - Lists loaded extensions.
* `inform [message]` - Send a message to all the servers the bot is in.
* `load [extension]` - Loads an extension.
* `playing [game]` - Set the playing status of the bot.
* `reload [extension]` - Reloads an extension.
* `unload [extension]` - Unloads an extension.
* **Database** ([*RethinkDB*](https://www.rethinkdb.com/). is used for the bot. Aliases: `database`, `db`)
  * `db create [database]` - Creates a database.
  * `db delete [database]` - Deletes a database.
  * `db list [database]` - Lists all databases.
  * `db tablecreate [database] [table]` - Creates a table in a database. (Alias: `tc`)
* **Bot Profile** (A way to change the output of certain commands. Aliases:`botprofile`, `bp`)
  * `bp create` - Creates a bot profile.
  * `bp error [text]` - Edit the message when bot encounters an error. (A pair of curly brackets `{}` is needed)
  * `bp invite [text]` - Edit the output for `invite`.
  * `bp ping [text]` - Edit the output when the bot is pinged.
  * `bp server [text]` - Edit the output for `server`.
* **Help**
  * `help create [command] [text]` - Creates a help page.
  * `help list` - Lists all help pages.
  * `help remove [command]` - Removes a help page.
  * `help update [command] [text]` - Updates a help page.

## Formatting
Polar Bot features a formatting system that provides functionality and interactivity to commands such as tag and welcome. For example:

![Formatting Example](https://i.imgur.com/g5oroJD.png)

**This feature is inspired by [Bot 42](https://fennekid.github.io/beta/yna.html)*

### Tag Format Objects
* `{tag}` - Name of tag.
* `{me}` - Display name of caller.
* `{me-user}` - Username with discrimination number of caller.
* `{me-username}` - Username without discrimination number of caller.
* `{me-discrim}` - Discrimination number of caller.
* `{me-id}` - User ID of caller.
* `{channel}` - Name of channel the tag is called in.
* `{channel-id}` - ID of channel the tag is called in.
* `{server}` - Name of server the tag is called in.
* `{server-id}` - ID of server the tag is called in.
* `{freq}` - Number of times the tag was called.
* `{arg1}` - Optional argument 1.
* `{arg2}` - Optional argument 2.

### Welcome Format Objects
* `{me}` - Display name of new member.
* `{me-user}` - Username with discrimination number of new member.
* `{me-username}` - Username without discrimination number of new member.
* `{me-discrim}` - Discrimination number of new member.
* `{me-id}` - User ID of new member.
* `{channel}` - Name of channel the welcome message is called in.
* `{channel-id}` - ID of channel the welcome message is called in.
* `{server}` - Name of server the welcome message is called in.
* `{server-id}` - ID of server the welcome message is called in.

### Tips and Tricks
* To ping someone, do `<@{me-id}>`.
* To link a channel, do `<#{channel-id}>`