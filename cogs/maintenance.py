import discord
from discord.ext import commands
import os
import subprocess
import sys

OWNER_IDS = [718869485548994664, 272872244299038720, 143792779913461760]


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update(self, ctx):
        if ctx.author.id in OWNER_IDS:
            await ctx.send("Pulling the latest updates from GitHub...")
            git_pull = subprocess.run(
                ["git", "pull"], capture_output=True, text=True)
            if git_pull.returncode == 0:
                await ctx.send("Successfully pulled the latest updates. Restarting bot...")
                await ctx.send("Bot is restarting...")
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                await ctx.send(f"Error pulling updates: {git_pull.stderr}")
        else:
            await ctx.send("You do not have permission to run this command.")


async def setup(bot):
    await bot.add_cog(Maintenance(bot))
