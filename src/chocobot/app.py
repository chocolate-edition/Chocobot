"""main entrypoint for the app"""
import os
import sys
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

    # Prevent spam (2 or more identical messages in a row)
    messages: list[discord.Message] = [msg async for msg in message.channel.history(limit=2)]
    if all(msg.content == message.content for msg in messages):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please don't spam!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx: commands.Context[Any]) -> None:
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def matrix(ctx: commands.Context[Any]) -> None:
    await ctx.send('''
**How do I use Matrix Enchanting?**
You can generate \"enchantment pieces\" using XP and Lapis and place them on a grid. Two pieces of the same type can be merged to upgrade the piece\'s level by placing one piece on top of the other. You can influence what kind of pieces you get using candles.

**Why can't I take my item out?**
Either you have incompatible enchantments (like Fortune/Silk Touch) or you have two of the same enchantments on the table. For the latter, remember that you can combine same-enchantment blocks to upgrade them.

**How do bookshelves influence Matrix Enchanting?**
Bookshelves increases the maximum amount of "blocks" you can create.

**What is candle influencing?**
Different coloured candles can influence the likelihood of an enchantment being rolled. For specific information, use `!candles`''')

@bot.command()
async def candles(ctx: commands.Context[Any]) -> None:
    await ctx.send('''
__**Here's how different coloured candles influence the Matrix Enchantment system!**__
White: Unbreaking
Orange: Fire Protection, Torrent, Lavewaxed
Magenta: Knockback, Punch, Bolok's Furry, Sharpshooter, Backstabbing, Straddle Jump
Light Blue: Feather Falling
Yellow: Looting, Fortune, Luck of the Sea
Lime: Blast Protection
Pink: Silk Touch, Channeling
Gray: Bane of Arthropods
Light Gray: Protection,  Serpent Charmer
Cyan: Respiration, Loyalty, Infinity, Ceaseless, Returning Board
Purple: Sweeping Edge, Multishot
Blue: Efficiency, Sharpness, Lure, Power, Impaling, Quick Charge
Brown: Aqua Affinity, Depth Strider, Riptide
Green: Thorns, Piercing
Red: Fire Aspect, Flame
Black: Smite, Projectile Protection''')

@bot.command()
async def spark(ctx: commands.Context[Any]) -> None:
    await ctx.send('''
**Please use the following command in-game:**
/spark profiler start --thread * --timeout 50''')

@bot.command()
async def latest(ctx: commands.Context[Any]) -> None:
    await ctx.send('''
**Start Minecraft:** Open Minecraft and play until you encounter the crash/error. Close Minecraft and keep it closed.

**Find Logs:**
     **For Vanilla Minecraft (Mojang Launcher):** Open the folder where Minecraft stores its files. On Windows, it's usually
     located at `%appdata%\\.minecraft`. On macOS, find it at `~/Library/Application Support/minecraft`.

     **For CurseForge:** If you're using CurseForge, click on your modpack within CurseForge's launcher. Then click on the
     three dots (...) on the right-hand side and choose "Open Folder."

     **For Prisim Launcher:** If you're using the Prisim Launcher, click on the modpack you're using. On the right side of the
     launcher, click "Open .minecraft."

     **For AtLauncher:** If you're using AtLauncher, go to the modpack you are using, then click on the "Open Folder" button.

**Open Log File:** Inside the modpack's folder, locate the "logs" folder. Find the file named "latest" or "latest.log" within the "logs" folder and open it with Notepad by double-clicking.

**Copy Contents:** Select everything in the file (Ctrl-A or Cmd-A), then copy it (Ctrl-C or Cmd-C).

**Use mclo.gs:** Go to https://mclo.gs/, paste the contents (Ctrl-V or Cmd-V) into the large field or add the file.

**Submit and Share:** Click "Submit Anonymously." After submitting, copy the URL from the address bar and share it in ⁠https://discord.com/channels/945364406609514517/1139306430046949498 to the person who needs the log. Wait for further instructions.''')

@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context[Any])-> None:
    await ctx.send('Shutting Down!')
    sys.exit(0)

def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()