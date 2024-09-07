"""main entrypoint for the app"""
import os
import sys
from chocobot.constants import constants
from typing import Any
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN: str = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    if any(role.name == 'admin' for role in message.author.roles):
        await bot.process_commands(message)
        return

    # Prevent spam (2 or more identical messages in a row)
    messages: list[discord.Message] = [msg async for msg in message.channel.history(limit=2)]
    if all(msg.content == message.content and msg.author == message.author for msg in messages):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please don't spam!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx: commands.Context[Any]) -> None:
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def matrix(ctx: commands.Context[Any]) -> None:
    await ctx.send(constants.MATRIX_RESPONSE)

@bot.command()
async def candles(ctx: commands.Context[Any]) -> None:
    await ctx.send(constants.CANDLES_RESPONSE)

@bot.command()
async def spark(ctx: commands.Context[Any]) -> None:
    await ctx.send(constants.SPARK_RESPONSE)

@bot.command()
async def log(ctx: commands.Context[Any]) -> None:
    await ctx.send(constants.LOG_RESPONSE)

@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context[Any]) -> None:
    await ctx.send('Shutting Down!')
    sys.exit(0)

def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()