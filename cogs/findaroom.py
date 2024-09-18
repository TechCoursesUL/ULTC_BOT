import discord
from discord import app_commands
from discord.ext import commands
import os
import subprocess
import sys

from errorhandler import ErrorHandler

class FindARoom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.building_acronyms = {
            "Schuman Building": (["SG", "S1", "S2"], "https://maps.app.goo.gl/dwgzdSP9WXfgHuQm8"),
            "Kemmy Business School": (["KBG", "KB1", "KB2", "KB3"], "https://maps.app.goo.gl/owHGAn8NJqELBYuw8"),
            "Computer Science Building": (["CSG", "CS1", "CS2", "CS3"], "https://maps.app.goo.gl/5PwH5nKDr2H5HQ9F6"),
            "Glucksman Library and Information Services Building": (["GLG", "GL0", "GL1", "GL2"], "https://maps.app.goo.gl/BXtFYB6Bi9JMfim58"),
            "Foundation Building": (["FB", "FG", "F1", "F2"], "https://maps.app.goo.gl/CMGNow2w8JKCLs1w7"),
            "Engineering Research Building": (["ERB", "ER0", "ER1", "ER2"], "https://maps.app.goo.gl/g22HtvqEsr3fwKZv6"),
            "Languages Building": (["LCB", "LC0", "LC1", "LC2"], "https://maps.app.goo.gl/tw9yQL3bqEVmVeTX7"),
            "Lonsdale Building": (["LB", "LG", "L1", "L2"], "https://maps.app.goo.gl/wMyurRMW8e1FmSy47"),
            "Schrodinger Building": (["SR1", "SR2", "SR3"], "https://maps.app.goo.gl/ez6eqtVKUss1yoWp9"),
            "PESS Building": (["PG", "PM", "P1", "P2"], "https://maps.app.goo.gl/XAakN9zxL6HfZQk1A"),
            "Health Sciences Building": (["HSG", "HS1", "HS2", "HS3"], "https://maps.app.goo.gl/jLw5HmNYi3JUNpvi6"),
            "Main Building BLOCK A": (["A0", "AM", "A1", "A2", "A3"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK B": (["B0", "BM", "B1", "B2", "B3"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK C": (["CG", "C0", "CM", "C1", "C2"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK D": (["DG", "D0", "DM", "D1", "D2"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK E": (["EG", "E0", "EM", "E1", "E2"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Analog Building": (["AD0", "AD1", "AD2", "AD3"], "https://maps.app.goo.gl/xN34mcRj32H2ndsy5"),
            "Irish World Academy Building": (["IWG", "IW1", "IW2"], "https://maps.app.goo.gl/KEfpwx7rcWiAP3JaA")
        }

    @app_commands.command(description="find a room by it's identifier")
    @ErrorHandler
    async def findaroom(self, interaction : discord.Interaction, location: str):
        building_name = None
        room_number = None
        maps_link = None

        for building, (acronyms, link) in self.building_acronyms.items():
            for acronym in acronyms:

                if location.lower().startswith(acronym.lower()):

                    room_number = location[len(acronym):]
                    building_name = building
                    maps_link = link
                    break
            if building_name:
                break

        if not building_name:
            raise KeyError(f"Unknown building acronym. Please check the input: {location}.")
            

        if not room_number or not room_number.isdigit():
            raise KeyError(f"Invalid room number for the location: {location}.")
            

        floor_number = room_number[0]

        embed = discord.Embed(
            title="Room Location Found!",
            description=f"Here is the location for `{location}`:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Building", value=building_name, inline=False)
        embed.add_field(name="Floor", value=f"Floor {floor_number}", inline=True)
        embed.add_field(name="Room", value=f"Room {room_number}", inline=True)
        embed.add_field(name="Google link", value=f"{maps_link}", inline=False)

        embed.set_footer(
            text="although unlikely, if this bot is incorrect please report it to us.")

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FindARoom(bot))
