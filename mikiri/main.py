import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
token = os.getenv("TOKEN")

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
        await self.tree.sync(guild=DEV_GUILD)

bot = MyBot()

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


bot.run(token)