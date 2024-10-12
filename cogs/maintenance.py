import discord
from discord import app_commands
from discord.ext import commands
from permissions import Permissions
from errorhandler import ErrorHandler
import os
import subprocess
import sys

OWNER_IDS = [718869485548994664, 272872244299038720, 143792779913461760]


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Manually update the bot to the latest version")
    @ErrorHandler
    async def update(self, interaction: discord.Interaction):
        await Permissions.ValidatePermission("update", interaction.user)
        message = await interaction.channel.send(
            "Pulling the latest updates from GitHub..."
        )
        git_pull = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if git_pull.returncode == 0:
            await message.edit(
                content="Successfully pulled the latest updates. Restarting bot..."
            )
            await message.delete()
            await interaction.followup.send("Bot is restarting...")
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            await message.delete()
            raise ValueError(f"Error pulling updates: {git_pull.stderr}")


async def setup(bot):
    await bot.add_cog(Maintenance(bot))
