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
    
    @commands.command()
    async def sync(self, ctx):
        synced = await self.bot.tree.sync()
        await ctx.send(f"{synced} slash command(s) synced")

    @commands.command()
    async def version(self, ctx):
        version = None
        try:
            version = open('version.txt').read().strip()
        except FileNotFoundError:
            version = "Version file not found"
        await ctx.send(f"bot currently running on branch: {version}")
    
    @tasks.loop(seconds=30)
    async def heartbeat(self):
        request = requests.get("https://ultc-bot.onrender.com/")
        print(request.text)
    


async def setup(bot):
    await bot.add_cog(General(bot))
