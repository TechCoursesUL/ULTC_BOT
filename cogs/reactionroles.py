import discord
from discord import app_commands
from discord.ext import commands
from permissions import Permissions


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = {
            "🖥️": "1283817589788770414",
            "🔐": "1283820720128000120",
            "🎮": "1283820769662603285",
            "🤖": "1283820892698312858",
            "🤓": "1283820845625639005",
            "💾": "1283820666830983258",
            "🎉": "1284937266308976770",
        }
        self.optOutReactions = [
            '🎉',
        ]


    @app_commands.command()
    async def setup_reactions(self, interaction: discord.Interaction):
        message = await interaction.channel.send(
            """
React to this message to get a role!
Common entry: 🖥️
Cyber Security: 🔐
Game Development: 🎮
AI and Machine Learning: 🤖
Immersive Software Engineering: 🤓
Computer Systems: 💾
Annoucements (opt out): 🎉"""
        )

        for emoji in self.reactions:
            await message.add_reaction(emoji)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.optOutReactions.__contains__(str(payload.emoji)):
            await self.check_reaction(payload, add_role=False)
        else:
            await self.check_reaction(payload, add_role=True)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.optOutReactions.__contains__(str(payload.emoji)):
            await self.check_reaction(payload, add_role=True)
        else:
            await self.check_reaction(payload, add_role=False)


    async def check_reaction(self, payload, add_role):
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        member = guild.get_member(payload.user_id)
        if channel.name != "roles":
            return
        if member.bot:
            return
        if str(payload.emoji) not in self.reactions:
            return
        role_id = self.reactions[str(payload.emoji)]
        role = channel.guild.get_role(int(role_id))
        if add_role:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)
            

                    
async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
