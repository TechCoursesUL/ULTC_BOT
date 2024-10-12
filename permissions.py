import discord


class Permissions:

    perms = {
        "punishprotectionbypass": [
            1283864386305527930,  # Founders
        ],
        "giveAllRoles": [
            1283864386305527930,  # Founders
        ],
        "punishprotection": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
            1283828417707642965,  # Beep Boop (bots)
        ],
        "kick": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "ban":  [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "unban":  [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "mute": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "getallbandata": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "getuserbandata": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "update": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
        ],
        "load": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ],
        "create_embed": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
        ],
        "purge": [
            1283864386305527930,  # Founders
            1283787573742927882,  # Admins
            1284246744800039055,  # ModerationPerms
        ]
    }

    @staticmethod
    async def _ValidatePermission(permission: str, commandUser: discord.Member) -> bool:
        if not Permissions.perms.__contains__(permission):
            raise FileNotFoundError("Command attempted to be validated does not exist in Moderation.perms")

        return any(
            discord.utils.get(commandUser.guild.roles, id=role)
            in commandUser.roles
            for role in Permissions.perms[permission]
        )

    @staticmethod
    async def ValidatePermission(permission: str, commandUser: discord.Member) -> bool:
        if await Permissions._ValidatePermission(permission, commandUser):
            return True
        else:
            raise PermissionError("Missing Permissions")
