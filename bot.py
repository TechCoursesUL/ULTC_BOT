import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import webserver
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
load_dotenv()

@bot.command(name="sync")
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s) synced")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('TOKEN'))


webserver.keep_alive()

asyncio.run(main())
