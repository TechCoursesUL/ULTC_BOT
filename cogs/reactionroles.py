import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = 1284937490800578632
        self.channel_id = 1283817759540510720
        self.emoji_role_map = {
            '🖥️': 1283817589788770414,
            '🔐': 1283820720128000120,
            '🎮': 1283820769662603285,
            '🤖': 1283820892698312858,
            '🤓': 1283820845625639005,
            '💾': 1283820666830983258,
            '🎉': 1284937266308976770,
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_id = self.emoji_role_map.get(str(payload.emoji))
        if not role_id:
            return

        role = guild.get_role(role_id)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if not member:
            return

        if member.bot:
            return

        try:
            await member.add_roles(role)
        except discord.HTTPException as e:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_id = self.emoji_role_map.get(str(payload.emoji))
        if not role_id:
            return

        role = guild.get_role(role_id)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if not member:
            return

        if member.bot:
            return

        try:
            await member.remove_roles(role)
        except discord.HTTPException as e:
            return
    
    @commands.command()
    async def setup_reactions(self, ctx):
        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        for emoji in self.emoji_role_map.keys():
            await message.add_reaction(emoji)
            


async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
