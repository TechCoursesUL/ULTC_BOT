import discord
import psutil
import time
import datetime
from permissions import Permissions
from errorhandler import ErrorHandler
from discord.ext import commands, tasks
from discord import app_commands
from typing import Literal, Optional
import requests


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        
    @app_commands.command(description="Displays server load info")
    @ErrorHandler
    async def load(self, interaction: discord.Interaction):
        await Permissions.ValidatePermission("load", interaction.user)
        
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        
        
        embed = discord.Embed(
            title="📊 Current Server Load",
            color=0x33d17a,
            description="Here's the current status of the server's performance."
        )
        
        embed.add_field(name="**🖥️ CPU Usage**", value=f"`{psutil.cpu_percent()}%`", inline=False)
        embed.add_field(name="**💾 RAM Usage**", value=f"`{psutil.virtual_memory().percent}%`", inline=False)
        embed.add_field(name="**🕒 Uptime**", value=f"`{uptime_str}`", inline=False)
        embed.add_field(name="**📂 Disk Usage**", value=f"`{psutil.disk_usage('/').percent}%`", inline=False)
        embed.set_footer(text=f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(description="creates a single-line (for now) embed in the current channel.")
    @ErrorHandler
    async def create_embed(self, interaction: discord.Interaction, title: str, description: str, hexcolour: str):
        await Permissions.ValidatePermission("create_embed", interaction.user)
        
        print(discord.Color.from_str(hexcolour.strip()))
        
        
        embed = discord.Embed(title=title, description=description,
                              color=discord.Color.from_str(hexcolour.strip()))
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command()
    @ErrorHandler
    async def purge(self, interaction: discord.Interaction, amount: int):
        await Permissions.ValidatePermission("purge", interaction.user)
        
        await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Successfully deleted {amount} messages")
        
    @app_commands.command()
    @ErrorHandler
    async def version(self, interaction: discord.Interaction):
        version = open('version.txt').read().strip()
        
        await interaction.followup.send(f"bot currently running on version: {version}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is online.")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            role = member.guild.get_role(1284937266308976770)
            member.add_roles(role)
            
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.content.startswith('!') and message.content != "!sync":
            await message.channel.send("this bot no longer uses the ! command prefix, please use /")


async def setup(bot):
    await bot.add_cog(General(bot))
