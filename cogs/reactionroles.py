import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = {
            '🖥️': '1283817589788770414',
            '🔐': '1283820720128000120',
            '🎮': '1283820769662603285',
            '🤖': '1283820892698312858',
            '🤓': '1283820845625639005'
        }

    @commands.command()
    async def setup_reactions(self, ctx):
        message = await ctx.send('''
React to this message to get a role!
Common entry: 🖥️
Cyber Security: 🔐
Game Development: 🎮
AI and Machine Learning: 🤖
Immersive Software Engineering: 🤓''')

        for emoji in self.reactions:
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.check_reaction(reaction, user, add_role=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.check_reaction(reaction, user, add_role=False)

    async def check_reaction(self, reaction, user, add_role):
        if user.bot:
            return
        if reaction.emoji not in self.reactions:
            return

        role_id = self.reactions[reaction.emoji]
        if role := discord.utils.get(
            reaction.message.guild.roles, id=int(role_id)
        ):
            if member := reaction.message.guild.get_member(user.id):
                if add_role:
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
