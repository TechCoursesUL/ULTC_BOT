import discord
from discord.ext import commands


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_reactions(self, ctx):
        message = await ctx.send('''React to this message to get a role!<br>
                                 Common entry: 🖥️<br>
                                 Cyber Security: 🔐<br>
                                 Game Development: 🎮<br>
                                 AI and Machine Learning: 🤖<br>
                                 Immersive Software Engineering: 🤓<br>''')

        reactions = {
            '🖥️': '1283817589788770414',
            '🔐': '1283820720128000120',
            '🎮': '1283820769662603285',
            '🤖': '1283820892698312858',
            '🤓': '1283820845625639005'
        }

        for emoji in reactions:
            await message.add_reaction(emoji)

        async def check_reaction(reaction, user):
            if user.bot:
                return
            if reaction.message.id != message.id:
                return
            if reaction.emoji not in reactions:
                return

            role_name = reactions[reaction.emoji]
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                member = ctx.guild.get_member(user.id)
                if member:
                    await member.add_roles(role)

        # Register the reaction event listener
        self.bot.event(check_reaction)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.check_reaction(reaction, user)

    async def check_reaction(self, reaction, user):
        if user.bot:
            return
        if reaction.emoji not in self.reactions:
            return

        role_name = self.reactions[reaction.emoji]
        role = discord.utils.get(reaction.message.guild.roles, name=role_name)
        if role:
            member = reaction.message.guild.get_member(user.id)
            if member:
                await member.add_roles(role)


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
