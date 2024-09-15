import discord
from discord.ext import commands
import logging


class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = 1284648528395636737
        self.emoji_role_map = {
            '🖥️': 1283817589788770414,
            '🔐': 1283820720128000120,
            '🎮': 1283820769662603285,
            '🤖': 1283820892698312858,
            '🤓': 1283820845625639005,
            '💾': 1283820666830983258
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            logging.warning(f"Guild not found for ID: {payload.guild_id}")
            return

        role_id = self.emoji_role_map.get(str(payload.emoji))
        if not role_id:
            logging.warning(f"Role not mapped for emoji: {payload.emoji}")
            return

        role = guild.get_role(role_id)
        if not role:
            logging.warning(f"Role not found for ID: {role_id}")
            return

        member = guild.get_member(payload.user_id)
        if not member:
            logging.warning(f"Member not found for ID: {payload.user_id}")
            return

        if member.bot:
            return

        try:
            await member.add_roles(role)
            logging.info(f"Assigned role {role.name} to {member.display_name}")
        except discord.HTTPException as e:
            logging.error(f"Failed to add role: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            logging.warning(f"Guild not found for ID: {payload.guild_id}")
            return

        role_id = self.emoji_role_map.get(str(payload.emoji))
        if not role_id:
            logging.warning(f"Role not mapped for emoji: {payload.emoji}")
            return

        role = guild.get_role(role_id)
        if not role:
            logging.warning(f"Role not found for ID: {role_id}")
            return

        member = guild.get_member(payload.user_id)
        if not member:
            logging.warning(f"Member not found for ID: {payload.user_id}")
            return

        if member.bot:
            return

        try:
            await member.remove_roles(role)
            logging.info(f"Removed role {role.name} from {
                         member.display_name}")
        except discord.HTTPException as e:
            logging.error(f"Failed to remove role: {e}")


async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
