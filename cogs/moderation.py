import discord
import firebase_admin
import functools
import random
import asyncio

import inspect

from discord.ext import commands
from discord import app_commands, Interaction
from db import ULTCDB



class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Perms = {
            "punishprotectionbypass": [
                1283864386305527930, # Founders
            ],
            "punishprotection": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
                1283828417707642965, # Beep Boop (bots)
            ],
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
            ],
            "GetBannedUsers": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ]
        }
        self.db = ULTCDB()
    
    def HandleErrors(f):
        async def decorator(ctx, *args, **kwargs):
            try:
                await f(ctx, *args, **kwargs)
            except Exception as e:
                await args[0].response.send_message(f"(decorator) Command Failed- {e}")  
                
        decorator.__name__ = f.__name__
        sig = inspect.signature(f)
        decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])  # from ctx onward
        return decorator
    

    async def SendResponse(self, interaction: discord.Interaction, message: str):
        interaction.response.send_message(message)
        
    async def _ValidatePermission(self, permission: str, commandUser: discord.Member) -> bool:        
        for role in self.Perms[permission]:
            if discord.utils.get(commandUser.guild.roles, id=role) in commandUser.roles:
                return True
            
        return False
    async def ValidatePermission(self, permission: str, commandUser: discord.Member) -> bool:        
        if self.ValidatePermission(permission, commandUser):
            return True
        else:    
            raise PermissionError("Missing Permissions")
                         
    
    async def ValidatePunishPermissions(self, command: str, commandUser: discord.Member, targetUser: discord.Member) -> str:
        error = None
        
        if await self._ValidatePermission("punishprotection", targetUser):
            error = PermissionError("User is protected")
        
        if await self._ValidatePermission(command, commandUser):
            if error == None:
                return "Successfully"
            
            elif await self._ValidatePermission("punishprotectionbypass", commandUser):
                return "User is protected- but your role allows a bypass. Successfully" #TODO: add confirmation prompt before bypass
            
        if not error:
            raise PermissionError("Missing Permissions")
        else:
            raise error
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("The dawg doesn't exist dawg")   
        
    
    @app_commands.command(description="kick a user")
    @HandleErrors
    async def kick(self, interaction: discord.Interaction, target: discord.Member, reason: str):
        logMessage = await self.ValidatePunishPermissions("kick", interaction.user, target)
        
        await interaction.response.send_message(f"{logMessage} kicked {target.global_name} for {reason}")
        
    
    @app_commands.command(description="ban a user")
    #@HandleErrors
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str, dayDuration: int):
        logMessage = await self.ValidatePunishPermissions("ban", interaction.user, member)
            
        await interaction.response.send_message(f"{logMessage} banned {member.global_name} for {dayDuration} day(s) for {reason}")
        
                
    #@app_commands.command(description="Get a list of all banned users")
    #@HandleErrors
    #async def getbannedusers(self, interaction: discord.Interaction):
    #    await self.ValidatePermission("GetBannedUsers", interaction.user)
    #
    #   await interaction.response.send_message(f"Banned Users: {self.db.GetBannedUsers()}")
    
            
            
        
    
            
        
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
