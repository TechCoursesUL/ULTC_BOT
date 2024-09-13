import discord
from discord.ext import commands
from discord import app_commands, Interaction


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(description="responds with your roles (slash commands test)")
    async def getroles(self, interaction: discord.Interaction):
        await interaction.response.send_message( str(interaction.user.roles) , ephemeral= True)
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
