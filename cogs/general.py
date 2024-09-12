import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is online.")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("idk lol?")


async def setup(bot):
    await bot.add_cog(General(bot))
