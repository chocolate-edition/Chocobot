"""main entrypoint for the app"""
import os
import sys
import requests
import html2text
from chocobot.constants import constants
from chocobot.curseforge import curseforge
from typing import Any
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN: str = os.environ['DISCORD_TOKEN']
CF_TOKEN: str = os.environ['CURSE_FORGE_TOKEN']
CF_PROJECT_ID = '888414'

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': CF_TOKEN
}

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

cf_file_data = requests.get('https://api.curseforge.com/v1/mods/'+ CF_PROJECT_ID +'/files', headers = headers).json()
file_ID = str(cf_file_data['data'][0]['id'])
cf_link ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + file_ID

cf_change_log = requests.get('https://api.curseforge.com/v1/mods/'+ CF_PROJECT_ID +'/files/' + file_ID + '/changelog', headers = headers).json()
change_log = html2text.html2text(str(cf_change_log['data']))


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected to Discord!')
   # curseforge.update_cf()



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
    """The new enchanting system"""
    await ctx.send(constants.MATRIX_RESPONSE)

@bot.command()
async def candles(ctx: commands.Context[Any]) -> None:
    """The influences of each candle"""
    await ctx.send(constants.CANDLES_RESPONSE)

@bot.command()
async def spark(ctx: commands.Context[Any]) -> None:
    """How to create a spark report"""
    await ctx.send(constants.SPARK_RESPONSE)

@bot.command()
async def log(ctx: commands.Context[Any]) -> None:
    """How to get your latest log"""
    await ctx.send(constants.LOG_RESPONSE)

@bot.command()
async def link(ctx: commands.Context[Any]) -> None:
    await ctx.send(cf_link)

@bot.command()
async def changelog(ctx: commands.Context[Any]) -> None:
    await ctx.send(change_log)

@bot.command()
async def debug(ctx: commands.Context[Any]) -> None:
    await ctx.send(file_ID)

async def java(ctx: commands.Context[Any]) -> None:
    """Link to proper java version"""
    await ctx.send(constants.JAVA_RESPONSE)

@bot.command()
async def cdu(ctx: commands.Context[Any]) -> None:
    """Link to the offical server's discord"""
    await ctx.send(constants.CDU_RESPONSE)

@bot.command()
async def mclogs(ctx: commands.Context[Any]) -> None:
    """Link to the mclogs website"""
    await ctx.send(constants.MCLOGS_RESPONSE)

@bot.command()
async def eyes(ctx: commands.Context[Any]) -> None:
    """Explains the eyes and locked items"""
    await ctx.send(constants.EYES_RESPONSE)


@bot.command()
async def client(ctx: commands.Context[Any]) -> None:
    """Link to the latest client pack"""
    await ctx.send(curseforge.get_client_file())

@bot.command()
async def server(ctx: commands.Context[Any]) -> None:
    """Link to the latest server pack"""
    await ctx.send(curseforge.get_server_file())

@bot.command()
async def changelog(ctx: commands.Context[Any]) -> None:
    """The latest changelog"""
    await ctx.send(curseforge.get_change_log())

@bot.command()
async def downloads(ctx: commands.Context[Any]) -> None:
    """The download count"""

    await ctx.send('The pack has ' + curseforge.get_downloads() + ' downloads')

@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context[Any]) -> None:
    """Shuts chocobot down"""
    await ctx.send('Shutting Down!')
    sys.exit(0)

@bot.command()
@commands.is_owner()
async def updatecf(ctx: commands.Context[Any]) -> None:
    """Updates the CF link"""
    curseforge.update_cf()
    await ctx.send('Updated!')


def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()