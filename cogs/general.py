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
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")

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

@commands.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(General(bot))
