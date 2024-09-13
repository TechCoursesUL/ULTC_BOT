import discord
from discord.ext import commands
from discord import app_commands, Interaction


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @app_commands.tree.command(name="getroles", description="responds with your roles (slash commands test)")
    @app_commands.checks.has_role(1284246744800039055) #"ModeratorPerms" role, placeholder until proper role system is developed
    async def kick(self, interaction:discord.Interaction):
        await interaction.response.send_message( str(interaction.user.roles) , ephemeral= True)
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
