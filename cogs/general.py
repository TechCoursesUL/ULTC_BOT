import discord
from discord.ext import commands, tasks
from typing import Literal, Optional
import requests


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.heartbeat.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is online.")
    
    #@commands.Cog.listener()
    async def on_member_join(self, member):
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")


    @tasks.loop(seconds=30)
    async def heartbeat(self):
        request = requests.get("https://ultc-botdev.onrender.com/")
        print(request.text)


async def setup(bot):
    await bot.add_cog(General(bot))
