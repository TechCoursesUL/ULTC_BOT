import discord
import firebase_admin
from discord.ext import commands
from discord import app_commands, Interaction


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CommandPerms = {
            "kick": [
                        1283864386305527930, # Founders
                        1284246744800039055, # ModerationPerms
                    ],
            "ban":  [
                        1283864386305527930, # Founders
                        1284246744800039055, # ModerationPerms
                    ],
            "mute": [
                        1283864386305527930, # Founders
                        1284246744800039055, # ModerationPerms
                    ]
        }
    
    def ValidatePermissions(self, command: str, userRoles) -> bool:
        for Role in self.CommandPerms[command]:
            if userRoles.__contains__(Role):
                return True
        return False
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("the dawg doesn't exist dawg")   
        
    
    @app_commands.command(description="kick a user")
    async def kick(self, interaction: discord.Interaction, user: discord.Member):
        if self.ValidatePermissions("kick", interaction.user.roles):
            await interaction.response.send_message(f"successfully kicked {user.name} (lie)")
        else: interaction.response.send_message("can't do that for ya dawg") 
        
    @app_commands.command(description="ban a user")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, hourDuration: int):
        if self.ValidatePermissions("kick", interaction.user.roles):
            await interaction.response.send_message(f"successfully kicked {user.name} (lie)")
        else: interaction.response.send_message("can't do that for ya dawg")        
        
    
            
        
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
