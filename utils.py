import discord


def get_role_by_name(guild: discord.Guild, name: str) -> discord.Role:
    return discord.utils.get(guild.roles, name=name)


def get_text_channel_by_name(guild: discord.Guild, name: str) -> discord.TextChannel:
    return discord.utils.get(guild.text_channels, name=name)


def format_text_channel_name(name: str) -> str:
    return name.lower().replace(" ", "-").replace("$", "")


async def create_voice_text_channel_role(guild: discord.Guild, name: str):
    await guild.create_role(name=name)


async def create_voice_text_channel(guild: discord.Guild, name: str, category: str):
    if not any(role.name == name for role in guild.roles):
        await create_voice_text_channel_role(guild, name)

    channel_role = get_role_by_name(guild, name)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel_role: discord.PermissionOverwrite()
    }

    await guild.create_text_channel(name, overwrites=overwrites, category=category)


async def remove_voice_text_channel(guild: discord.Guild, channel_name: str, role_name: str):
    text_channel = get_text_channel_by_name(guild, channel_name)
    await text_channel.delete()

    channel_role = get_role_by_name(guild, role_name)
    await channel_role.delete()
