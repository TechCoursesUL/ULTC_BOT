import discord
from discord.ext import commands


class FindARoom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.building_acronyms = {
            "Schuman Building": (["S"], "https://maps.app.goo.gl/dwgzdSP9WXfgHuQm8"),
            "Kemmy Business School": (["KB"], "https://maps.app.goo.gl/owHGAn8NJqELBYuw8"),
            "Computer Science Building": (["CS"], "https://maps.app.goo.gl/5PwH5nKDr2H5HQ9F6"),
            "Glucksman Library": (["GL"], "https://maps.app.goo.gl/BXtFYB6Bi9JMfim58"),
            "Foundation Building": (["F"], "https://maps.app.goo.gl/CMGNow2w8JKCLs1w7"),
            "Engineering Research Building": (["ER"], "https://maps.app.goo.gl/g22HtvqEsr3fwKZv6"),
            "Languages Building": (["LC"], "https://maps.app.goo.gl/tw9yQL3bqEVmVeTX7"),
            "Lonsdale Building": (["L"], "https://maps.app.goo.gl/wMyurRMW8e1FmSy47"),
            "Schrodinger Building": (["SR"], "https://maps.app.goo.gl/ez6eqtVKUss1yoWp9"),
            "PESS Building": (["P"], "https://maps.app.goo.gl/XAakN9zxL6HfZQk1A"),
            "Health Sciences Building": (["HS"], "https://maps.app.goo.gl/jLw5HmNYi3JUNpvi6"),
            "Main Building BLOCK A": (["A"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK B": (["B"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK C": (["C"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK D": (["D"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Main Building BLOCK E": (["E"], "https://maps.app.goo.gl/gVw4CikGzaymFqz26"),
            "Analog Building": (["AD"], "https://maps.app.goo.gl/xN34mcRj32H2ndsy5"),
            "Irish World Academy": (["IW"], "https://maps.app.goo.gl/KEfpwx7rcWiAP3JaA")
        }

    @commands.command()
    async def findaroom(self, ctx, location):

        location = location.strip().upper()

        building_name = None
        room_number = None
        maps_link = None

        for building, (acronyms, link) in self.building_acronyms.items():
            for acronym in acronyms:
                if location.startswith(acronym):
                    room_number = location[len(acronym):].strip()
                    building_name = building
                    maps_link = link
                    break
            if building_name:
                break

        if not building_name:
            await ctx.send(f"Unknown building acronym. Please check the input: `{location}`.")
            return

        if (
            not room_number
            or not room_number.isdigit()
            and room_number[0] not in {"G", "M", "O"}
        ):
            await ctx.send(f"Invalid room number for the location: `{location}`.")
            return

        floor_number = self.get_floor_number(room_number)

        embed = discord.Embed(
            title="Room Location Found!",
            description=f"Here is the location for `{location}`:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Building", value=building_name, inline=False)
        embed.add_field(name="Floor", value=f"{floor_number}", inline=True)
        embed.add_field(name="Room", value=f"Room {room_number[1:]}", inline=True)
        embed.add_field(name="Google link", value=f"{maps_link}", inline=False)
        embed.set_footer(text="If this information is incorrect, please report it to us.")
        await ctx.send(embed=embed)

    def get_floor_number(self, room_number):
        first_char = room_number[0]
        if first_char in {"G", "B", "O"}:
            return "Ground Floor"
        elif first_char == "M":
            return "Mezzanine"
        else:
            return f"Floor {first_char}"


async def setup(bot):
    await bot.add_cog(FindARoom(bot))
