import discord

from constants import CATEGORY_SUFFIX, DEFAULT_CATEGORY_NAME


def get_role_by_name(guild: discord.Guild, name: str) -> discord.Role:
    return discord.utils.get(guild.roles, name=name)


def get_text_channel_by_name(guild: discord.Guild, name: str) -> discord.TextChannel:
    return discord.utils.get(guild.text_channels, name=name)


def get_category_by_name(guild: discord.Guild, name: str) -> discord.CategoryChannel:
    return discord.utils.get(guild.categories, name=name)


def format_text_channel_name(name: str) -> str:
    return name.lower().replace(" ", "-").replace("$", "")


async def create_voice_text_channel_role(guild: discord.Guild, name: str):
    await guild.create_role(name=name)


async def get_text_channel_category(guild: discord.Guild, category: discord.CategoryChannel) -> discord.CategoryChannel:
    text_cat_name = f"{category.name}{CATEGORY_SUFFIX}" if category is not None else DEFAULT_CATEGORY_NAME
    text_cat_pos = category.position + 1 if category is not None else 0
    text_cat = get_category_by_name(guild, f"{category}{CATEGORY_SUFFIX}")
    if text_cat is None:
        text_cat = await guild.create_category(text_cat_name, position=text_cat_pos)
    return text_cat


async def create_voice_text_channel(guild: discord.Guild, name: str, voice_category: discord.CategoryChannel):
    if not any(role.name == name for role in guild.roles):
        await create_voice_text_channel_role(guild, name)
    category = await get_text_channel_category(guild, voice_category)

    channel_role = get_role_by_name(guild, name)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel_role: discord.PermissionOverwrite(read_messages=True)
    }

    await guild.create_text_channel(name, overwrites=overwrites, category=category)


async def remove_voice_text_channel(guild: discord.Guild, channel_name: str, role_name: str):
    text_channel = get_text_channel_by_name(guild, channel_name)
    await text_channel.delete()

    channel_role = get_role_by_name(guild, role_name)
    await channel_role.delete()
