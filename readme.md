# Polar Bot
A Discord bot designed for the [/r/Malaysia server](https://discord.gg/gCpJ9BF).

## Commands
* `[]` is a mandatory argument while `()` is an optional argument.

### General
* `+help` - Brings up the help page.
* `+me [message]` - An adoption of Skype's /me command.
* `+ping` - Pong!
* `+youtube [search]` - Returns a YouTube link. (Alias: `+yt`)

### Memory
* **Tag** (See [*Tag Format Objects*](https://github.com/polar-rex/Polar-Bot#tag-formatting). Aliases: `tag`, `t`)
  * `+tag [tag] (arg1) (arg2)` - Returns the content of the tag.
  * `+tag create [tag] [message] (arg1) (arg2)` - Creates a tag. `@here` or `@everyone` cannot be used in a tag.
  * `+tag delete [tag]` - Deletes a tag if you're the owner.
  * `+tag list (member)` - Returns a list of the member's tags. If no member is given, then the caller's tags are returned.
  
### Moderation
* `+ban [member]` - Bans a member. (Requires *Ban Members* permission)
* `+clear [number]` - Clears a number of recent messages from a channel. (Requires *Manage Messages* permission)
* `+kick [member]` - Kicks a member. (Requires *Kick Members* permission)
  
### Server Specific
* `+malaysian` - Gives user the Malaysian role.
* `+nonmalaysian` - Gives user the Non-Malaysian role.

### Bot Owner Only
* `+cogs` - Lists loaded extensions.
* `+load [cog]` - Loads an extension.
* `+playing [game]` - Set the playing status of the bot.
* `+reload [cog]` - Reloads an extension.
* `+unload [cog]` - Unloads an extension.

## Tag Formatting
Polar Bot features a formatting system that provides allows tags to be dynamic. For example:

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

### Tips and Tricks
* To ping someone, do `<@{me-id}>`.
* To link a channel, do `<#{channel-id}>`