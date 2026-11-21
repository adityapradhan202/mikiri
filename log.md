## 1. Basics

Go to OAuth2 URL generator tab in developer portal.  
Under scope: Select bot and application.commands for slash command.  
Initially give permissions like - send messsages, read message history, view channels, slash commands.

### 1.1 First discord bot.
```py
import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(TOKEN)
```
* discord.Intents.default() — Requests the default Gateway intents.
* discord.Client() — Creates a Discord client.
* @client.event — Registers an event handler.
* on_ready() — Called when the client is ready.
* client.run(TOKEN) — Starts the bot.

### 1.2 Understanding commands.Bot and events.

Code example:

```py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix="m!",
    intents=intents
)

# Message delete log chanenl ID
LOG_CHANNEL_ID = 1573607482641752154
MEMBER_REMOVE_CHANNEL_ID = 1573618423072690217

# Events

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event 
async def on_member_join(member):
    print(f"{member} joined!")


# Event handler to process incoming messages.
@bot.event
async def on_message(message):

    # This line is very important. 
    # Otherwise bot wil keep processing it's own messages, never ending loop
    if message.author == bot.user:
        return

    # Sends a message to the same channel
    # await message.channel.send("Hello!")
    if message.content == "hello" or message.content == "hi":
        await message.reply("Hi how are you doing!")

    print(f"Author of the message: {message.author.display_name}")
    print(f"Message content: {message.content}") 
    print(f"Channel where message was dropped: {message.channel}")

    # Recommended to put this line in the end
    # Because if something is a command that starts with prefix - run it
    await bot.process_commands(message)


# Creating an event handler which will log the deleted message to a specific channel
@bot.event
async def on_message_delete(message):

    if message.author == bot.user:
        return 
    channel = bot.get_channel(LOG_CHANNEL_ID)
    channel_message = f" Username - {message.author.name} | Display name - {message.author.display_name} | Deleted message: {message.content}"
    await channel.send(channel_message)


# Event handler when a message is edited
@bot.event
async def on_message_edit(before, after):
    # before and after stands for the message object before and after edit

    if before.author == bot.user:
        return
    # If there is no change in the edit, ignore it
    if before.content == after.content:
        return

    channel = bot.get_channel(LOG_CHANNEL_ID)
    channel_message = f"Display name - {before.author.display_name} | Before: {before.content} | After: {after.content}"
    await channel.send(channel_message)

# Event handler when member leaves
@bot.event
async def on_member_remove(member):

    channel = bot.get_channel(MEMBER_REMOVE_CHANNEL_ID)
    channel_message = f"{member.name} left the server!"
    await channel.send(channel_message)

def main() -> None:

    print("Bot is online!")
    bot.run(token)
    print(f"{bot.user.name} is offline!")
```

* `commands.Bot` is made on `discord.Client`, it gives the connection as well as the functionality to use a prefix to trigger prefix commands.
* `discord.Intents.default()` returns the default intents, except presences, members and message_content. For these exceptions, we need to set them as True manually in code. Search their meaning.
* `@bot.event` marks an async function as event handler.
* Functions like `on_message`, `on_message_edit`, `on_message_delete`, `on_member_remove` are all predefined event function in discord.py module.
* Must read the last line of `on_message` function and understand why this line has been written there.

### 1.3 Prefix command, context object, prefix command with args

See this code:

```py
@bot.command()
async def ping(ctx):
    # ctx stands for context
    await ctx.send("Pong!") # Sends Pong where m!ping command was called


@bot.command()
async def info(ctx):

    print(f"Author: {ctx.author.name}")
    print(f"Server: {ctx.guild}")
    print(f"Channel: {ctx.channel}")
    print(f"Prefix: {ctx.prefix}")

    await ctx.reply("Check console!")

@bot.command()
async def greet(ctx):
    await ctx.reply(f"Hello {ctx.author.mention}") # We can even mention

# Command with arguments
@bot.command()
async def greet_name(ctx, name):
    # by default name would be considered as string
    await ctx.send(f"Hello {name}")

# We can even take multiple arguments, default args are also possible
# Using type hint here automatically type casts the arguments
@bot.command()
async def multiply(ctx, a:int, b:int):
    await ctx.reply(a * b)

# Understand this syntax
@bot.command()
async def fullname(ctx, *, name):
    # This * means after the command whatever text is there, put that in name
    # Now if we don't use this * and pass "Bob White", it will consider Bob and white as different args
    await ctx.send(f"Hello {name}")

# Another example
@bot.command()
async def getinfo(ctx, age:int, *, name):
    await ctx.send(f"Your name is {name} and you are {age} years old!")
```

* ctx stands for context
* ctx contains info like - Which server, who executed the command, was it executed, what bot is handling?

Some properties and attributes we can access using ctx object.
```
ctx.author
ctx.guild
ctx.channel
ctx.bot
ctx.command
ctx.prefix
etc.
```