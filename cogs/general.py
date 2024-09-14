import discord
from discord.ext import commands, tasks
import requests


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.heartbeat.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is online.")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")
    
    @commands.command()
    async def sync(self, ctx):
        await ctx.send("Starting sync...")
        synced = await self.bot.tree.sync()
        await ctx.send(f"{synced} slash command(s) synced")

    @commands.command()
    async def version(self, ctx):
        version = None
        try:
            version = open('version.txt').read().strip()
        except FileNotFoundError:
            version = "Version file not found"
        await ctx.send(f"bot currently running on version: {version}")

    @tasks.loop(seconds=30)
    async def heartbeat(self):
        request = requests.get("https://ultc-botdev.onrender.com/")
        print(request.text)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")


async def setup(bot):
    await bot.add_cog(General(bot))
