Go to OAuth2 URL generator tab in developer portal.  
Under scope: Select bot and application.commands for slash command.  
Initially give permissions like - send messsages, read message history, view channels, slash commands.

### 1. First discord bot.
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

### 2. Understanding commands.Bot and events.

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

### 3. Prefix command, context object, prefix command with args

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

### 4. Error handling.

```py
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occurred: {error}")

# This runs when some error occurs while using commands
```

### 5. Slash commands basics and learning another way of initializing a bot.

```py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

# this is the id of discord server where we are developing
DEV_GUILD = discord.Object(id=1573584733588422829)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True

        super().__init__(
            command_prefix="!", intents=intents
        )

    async def setup_hook(self):

        # Use these two lines given in command if u accedetnly sync globally to all guilds
        # It takes a lot of time to update
        # To test rapidly use DEV_GUILD

        # self.tree.clear_commands(guild=None)   # clear GLOBAL commands only
        # await self.tree.sync()                 # push empty global list to Discord

        # sync the slash commands to the development guild
        await self.tree.sync(guild=DEV_GUILD)

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Prefix command
@bot.command()
async def hello(ctx):
    await ctx.send("Hello from prefix command!")

# You must mention the development server, to rapidly update it in the development server! (A must)
# Slash command
@bot.tree.command(name="ping", guild=DEV_GUILD)
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="bully", guild=DEV_GUILD)
async def bully(interaction:discord.Interaction):
    await interaction.response.send_message("Woahh... who the hell are you calling a bully yo?")

# discord.Interaction object is the central hub for handling everything that happens when a user triggers a slash command.
# With the help of interaction object we can access the following.


bot.run(token)
```

* `setup_hook() -> lifecycle function, it runs whatever is mentioned inside this function after the bots logs in and before the bot connects to the discord websocket(or gateway).
* Initialize db, sync slash commands globally, or for rapid development sync slash command to development server.


**This is how you can send arguments in slash command.**

```py
# name and str are required arguments
@bot.tree.command(name="greet", guild=DEV_GUILD)
async def greet(interaction:discord.Interaction, name:str, age:int):
    await interaction.response.send_message(f"Your name is {name}, you are {age} years old!")

# optional arguments
# to set argumetns as optional, make them default arguments, and set the default value to None
@bot.tree.command(name="vent", guild=DEV_GUILD)
async def vent(interaction:discord.Interaction, what_happend:str, about_you:str=None):
    message = ""
    if about_you:
        message += (about_you + "\n\n")
    message += f"What happened:\n{what_happend}"
    await interaction.response.send_message(message)

```


### 6. Cooldown on slash commands, and handling cooldown error.

Look at this code example.


```py

from discord import app_commands

# 1 time per 10 seconds, and key parameter stands for who gets their own cooldown
# Here individual user get their own cooldown.
@bot.tree.command(name="ping", guild=DEV_GUILD)
@app_commands.checks.cooldown(rate=1, per=10, key=lambda interaction: interaction.user.id)
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message("Pong!")

# Now if somebody hits the limit, it throws a cooldown error
# This is how we handle that error
# Use a decorator with the same name as the slash command
@ping.error
async def ping_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            content=f"Slow down try again later, after {error.retry_after} seconds!",
            # ephemeral means the user who invoked the command seens the message.
            ephemeral=True 
        )
```

### 7. Cogs

We can organise the code using cogs.

Project structure:
```
mikiri(main package)
|__ __init__.py
|__ main.py
|__ cogs
   |__ __init__.py
   |__ general.py
   |__ fun.py
   |__ config.py
```

Now the code.

**mikiri/cogs/config.py**

```py
from discord import Object

DEV_GUILD = Object(id=1575563960546234459)

```

**mikiri/cogs/general.py**

```py

import discord
from discord.ext import commands
from discord import app_commands

from mikiri.cogs.config import DEV_GUILD

# Inside cogs it is recommanded to use app_commands.command decorator.
# not bot.tree.command -> this registers it directly to bot's command tree.

class General(commands.Cog):

    # Takes the bot as argument for initialization
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="pings the bot")
    @app_commands.guilds(DEV_GUILD)
    async def ping(self, interaction:discord.Interaction):
        await interaction.response.send_message("Pong!")

# We will see 'load_extension' function in main.py
# That functon runs the setup function. This setup function connects the cogs to the bot.
async def setup(bot):
    await bot.add_cog(General(bot))


```


**mikiri/cogs/fun.py**

```py

import discord
from discord.ext import commands
from discord import app_commands
from mikiri.cogs.config import DEV_GUILD

import random


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice")
    @app_commands.guilds(DEV_GUILD)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Rolled the dice and you got a {random.randint(1,6)}")


async def setup(bot):
    await bot.add_cog(Fun(bot))

```


**mikiri/main.py**

```py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

from mikiri.cogs.config import DEV_GUILD

load_dotenv()
token = os.getenv("TOKEN")

class Mybot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.presences = True
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!", intents=intents
        )

    async def setup_hook(self):

        # load_extension function calls the setup function given inside the cogs
        await self.load_extension("mikiri.cogs.general") # mikiri is main package, general stands for general.py
        await self.load_extension("mikiri.cogs.fun")

        await self.tree.sync(guild=DEV_GUILD)


bot = Mybot()
bot.run(token)


```
