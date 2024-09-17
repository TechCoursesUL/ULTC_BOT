import discord
import dotenv
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
load_dotenv()

@bot.command()
async def sync(ctx):
    try:
        await ctx.send("Starting sync...")
        synced = await bot.tree.sync()
        await ctx.send(f"{synced} slash command(s) synced")
    except Exception as e:
        await ctx.send(f"An Error Occurred While Syncing: {e}")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())
