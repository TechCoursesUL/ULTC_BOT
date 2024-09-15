import discord
import dotenv
import os
import asyncio
import webserver
from discord.ext import commands
from dotenv import load_dotenv
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
load_dotenv()

@commands.command()
async def sync(self, ctx):
    ctx.send("Starting sync...")
    synced = await self.bot.tree.sync()
    ctx.send(f"{synced} slash command(s) synced")
@commands.command()
async def testsync(self, ctx):
    await ctx.send("Starting sync...")
    await ctx.send(f"{self.bot.tree.sync()}")

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
