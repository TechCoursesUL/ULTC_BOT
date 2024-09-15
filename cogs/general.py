import discord
from discord.ext import commands
import psutil
import time
import datetime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0

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

    @commands.command()
    async def load(self, ctx):
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
        await ctx.send(embed=embed)

    @commands.command()
    async def create_embed(self, ctx, *, args=None):
        if args is None:
            await ctx.send("Please provide the title, description, and color in the following format: `!embed <title> | <description> | <color>`")
            return
        try:
            title, description, colour = args.split('|')
            print(colour)
            print(discord.Color.from_str(colour.strip()))
        except ValueError:
            await ctx.send("Invalid format! Please use: `!embed <title> | <description> | <color> (in hex)`")
        embed = discord.Embed(title=title, description=description,
                              color=discord.Color.from_str(colour.strip()))
        print(title)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Successfully deleted {amount} messages")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if welcome_channel := discord.utils.get(
            member.guild.text_channels, name='welcome'
        ):
            await welcome_channel.send(f"Welcome to the server, {member.mention}! please checkout the rules and grab roles.")


async def setup(bot):
    await bot.add_cog(General(bot))
