import discord
import firebase_admin
import functools
import random
import asyncio
import time

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
            "unban":  [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ],
            "mute": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ],
            "getallbandata": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ],
            "getuserbandata": [
                1283864386305527930, # Founders
                1284246744800039055, # ModerationPerms
            ]
        }
        self.db = ULTCDB()
    
    def _ErrorHandler(f):
        async def decorator(*args, **kwargs):
            try:
                await args[1].response.defer()
                return await f(*args, **kwargs)
            except Exception as e:
                await args[1].followup.send(f"Command Failed- {e}")  
                
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
                confirmationmessage = await interaction.channel.send(f"[<!>]  {targetUser.name} is protected from /{command} -=-Your permission level allows a Bypass. Confirm Bypass? <(  **!confirmbypass**  <?>  **!cancelbypass**  )>-=-  [<!>]\n[<[ -=Auto-Cancels in 15 seconds=- ]>]")
                
                def check(m):
                    return (m.author.id == interaction.user.id and m.channel.id == interaction.channel.id and m.content in ("!confirmbypass", "!cancelbypass"))
                try:
                    response = await self.bot.wait_for('message', check=check, timeout=15)
                    await confirmationmessage.delete()
                    if response.content == "!confirmbypass":
                        return True
                    else:
                        raise ConnectionAbortedError("Command Cancelled")
                except asyncio.TimeoutError:
                    await confirmationmessage.delete()
                    raise TimeoutError("Command Auto-Cancelled")
                
                
        if not error:
            raise PermissionError("Missing Permissions")
        else:
            raise error
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("Member Not Found")   
        
    
    @app_commands.command(description="kick a user")
    @_ErrorHandler
    async def kick(self, interaction: discord.Interaction, target: discord.Member, reason: str):
        await self.ValidatePunishPermissions("kick", interaction, target)
        
        await interaction.followup.send(f"Kicked {target.global_name} for {reason}")
        
    
    @app_commands.command(description="ban a user")
    @_ErrorHandler
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str, dayduration: int):
        await self.ValidatePunishPermissions("ban", interaction, member)
            
        await self.db.AddBannedUser(member.id, member.global_name, int(time.time() + (86400 * dayduration)), reason)
        await interaction.followup.send(f"Banned {member.global_name} for {dayduration} day(s) for {reason}")
    
    @app_commands.command(description="unban a user")
    @_ErrorHandler
    async def unban(self, interaction: discord.Interaction, userid: int):
        await self.ValidatePermission("unban", interaction.user)
        
        await self.db.RemoveBannedUser(userid)
        await interaction.followup.send(f"Unbanned {userid}")
        
                
    @app_commands.command(description="Get database BanData of all banned users")
    @_ErrorHandler
    async def getallbandata(self, interaction: discord.Interaction):
        await self.ValidatePermission("getallbandata", interaction.user)
    
        await interaction.followup.send(f"All Banned Users BanData: {self.db.GetAllBannedUsers()}")
        
    @app_commands.command(description="Get database BanData of a banned user")
    @_ErrorHandler
    async def getuserbandata(self, interaction: discord.Interaction, userid : int):
        await self.ValidatePermission("getuserbandata", interaction.user)
    
        await interaction.followup.send(f"Banned User's BanData: {self.db.GetBannedUser(userid)}")
    
            
            
        
    
            
        
    
    
    


async def setup(bot):
    await bot.add_cog(Moderation(bot))
