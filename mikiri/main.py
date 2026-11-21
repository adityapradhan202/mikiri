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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
@bot.event 
async def on_member_join(member):
    print(f"{member} joined!")

# Event handler to process incoming messages.
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello" or message.content == "hi":
        await message.reply("Hi how are you doing!")
    await bot.process_commands(message)

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


def main() -> None:

    print("Bot is online!")
    bot.run(token)
    print(f"{bot.user.name} is offline!")


main()