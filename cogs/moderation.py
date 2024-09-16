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
            "getbannedusers": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ]
        }
        self.db = ULTCDB()
    
    def HandleErrors(f):
        async def decorator(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except Exception as e:
                await args[1].response.send_message(f"Command Failed- {e}")  
                
        decorator.__name__ = f.__name__
        sig = inspect.signature(f)
        decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])
        return decorator
    
        
    async def _ValidatePermission(self, permission: str, commandUser: discord.Member) -> bool:        
        for role in self.Perms[permission]:
            if discord.utils.get(commandUser.guild.roles, id=role) in commandUser.roles:
                return True
            
        return False
    async def ValidatePermission(self, permission: str, commandUser: discord.Member) -> bool:        
        if await self._ValidatePermission(permission, commandUser):
            return True
        else:    
            raise PermissionError("Missing Permissions")
                         
    
    async def ValidatePunishPermissions(self, command: str,  interaction: discord.Interaction, targetUser: discord.Member) -> bool:
        error = None
        
        if await self._ValidatePermission("punishprotection", targetUser):
            error = PermissionError(f"{targetUser.name} is protected from /{command}")
        
        if await self._ValidatePermission(command, interaction.user):
            if error == None:
                return True
            
            elif await self._ValidatePermission("punishprotectionbypass", interaction.user):
                timersecs = 15
                
                await interaction.response.defer()
                await interaction.channel.send(f"{targetUser.name} is protected from /{command}. Your permission level allows a bypass\nConfirm Bypass? ( **!confirmbypass** <?> **!cancelbypass** )\n[-Auto-Cancels in {timersecs} seconds-]")
                
                def check(m):
                    return (m.author.id == interaction.user.id and m.channel.id == interaction.channel.id and m.content in ("!confirmbypass", "!cancelbypass"))
                try:
                    response = await self.bot.wait_for('message', check=check, timeout=timersecs)
                    if response == "!confirmbypass":
                        return True
                    else:
                        raise ConnectionAbortedError("Command Cancelled")
                except asyncio.TimeoutError:
                    raise TimeoutError("Command Auto-Cancelled")
                
                
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
        logMessage = await self.ValidatePunishPermissions("kick", interaction, target)
        
        await interaction.response.send_message(f"Kicked {target.global_name} for {reason}")
        
    
    @app_commands.command(description="ban a user")
    @HandleErrors
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str, dayduration: int):
        logMessage = await self.ValidatePunishPermissions("ban", interaction.user, member)
            
        await interaction.response.send_message(f"Banned {member.global_name} for {dayduration} day(s) for {reason}")
        
                
    @app_commands.command(description="Get a list of all banned users")
    @HandleErrors
    async def getbannedusers(self, interaction: discord.Interaction):
        await self.ValidatePermission("getbannedusers", interaction.user)
    
        await interaction.response.send_message(f"Banned Users: {self.db.GetBannedUsers()}")
    
            
            
        
    
            
        
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
