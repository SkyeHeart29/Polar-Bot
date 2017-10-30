# Polar Bot
A polar bear Discord bot that stores tags, plays music, perform moderation functions and many other things. [**Invite Polar Bot to your server now***!](https://discordapp.com/oauth2/authorize?client_id=294708056112234497&scope=bot&permissions=406121544&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Fpolar-rex%2FPolar-Bot)

**Untick Administrator if you don't plan on using the moderation commands.*

## Notes
* To use a command, ping the bot or prefix with a full stop/period.
* Have any questions or problems regarding Polar Bot? Join [**The Arctic Den**](https://discord.gg/invite/5cxuTyN)! You'll also get a chance to try out the beta version of the bot.

## Commands
* `[]` is a mandatory argument while `()` is an optional argument.

### General
* `connections` - Shows the number of servers the bot is in.
* `help` - Shows the Github link.
* `invite` - Shows the invite link for Polar Bot.
* `ping` - Pong!
* `server` - Shows the invite link for The Arctic Den server.

### Moderation
* `ban [member]` - Bans a member. Caller requires *ban members* permission.
* `clear [number]` - Clears a number of recent messages from a channel. Caller requires *manage messages* permission.
* `kick [member]` - Kicks a member. Caller requires *kick members* permission.

### Recreational
* `me [message]` - An adoption of Skype's /me command.

### Memory
* **Tag** (See [Tag Formatting](https://github.com/polar-rex/Polar-Bot#tag-formatting). Aliases: `tag`, `t`)
  * `t [tag] (arg1) (arg2)` - Returns the content of the tag.
  * `t create [tag] [message] (arg1) (arg2)` - Creates a tag. `@here` or `@everyone` cannot be used in a tag.
  * `t delete [tag]` - Deletes a tag if you're the owner.
  * `t list (member)` - Returns a list of the member's tags. If no member is given, then the caller's tags are returned.

### Search
* `yt [search]` - Returns a YouTube link. (Alias: `youtube`)

### Voice
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
* **Database** (Aliases: `database`, `db`)
  * `db create [database]` - Creates a database.
  * `db delete [database]` - Deletes a database.
  * `db list [database]` - Lists all databases in the RethinkDB server.

## Tag Formatting
Polar Bot features a formatting system that provides functionality and interactivity to tags. For example:

![Tag Formatting](https://i.imgur.com/C53wob5.png)

**This feature is inspired by [Bot 42](https://fennekid.github.io/beta/yna.html)*

### Format Objects
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