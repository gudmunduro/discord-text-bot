import discord

from constants import CATEGORY_SUFFIX, DEFAULT_CATEGORY_NAME, CHANNEL_TAG_ROLE_NAME


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


async def get_channel_tag_role(guild: discord.Guild):
    if (role := get_role_by_name(guild, CHANNEL_TAG_ROLE_NAME)) is not None:
        return role

    return await guild.create_role(name=CHANNEL_TAG_ROLE_NAME)


async def is_created_by_bot(channel: discord.TextChannel):
    tag_role = await get_channel_tag_role(guild=channel.guild)
    return tag_role in channel.overwrites


async def is_bot_admin(user: discord.User):
    return True


async def get_text_channel_category(guild: discord.Guild, category: discord.CategoryChannel) -> discord.CategoryChannel:
    text_cat_name = f"{category.name}{CATEGORY_SUFFIX}" if category is not None else DEFAULT_CATEGORY_NAME
    text_cat_pos = category.position + 1 if category is not None else 0
    text_cat = get_category_by_name(guild, text_cat_name)
    if text_cat is None:
        text_cat = await guild.create_category(text_cat_name, position=text_cat_pos)
    return text_cat


async def create_voice_text_channel(guild: discord.Guild, name: str, voice_category: discord.CategoryChannel):
    if not any(role.name == name for role in guild.roles):
        await create_voice_text_channel_role(guild, name)
    category = await get_text_channel_category(guild, voice_category)

    channel_role = get_role_by_name(guild, name)
    channel_tag_role = await get_channel_tag_role(guild)  # Used to identify channels created by this bot
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel_role: discord.PermissionOverwrite(read_messages=True),
        channel_tag_role: discord.PermissionOverwrite(read_messages=False),
    }

    await guild.create_text_channel(name, overwrites=overwrites, category=category)


async def remove_voice_text_channel(guild: discord.Guild, channel_name: str, role_name: str):
    text_channel = get_text_channel_by_name(guild, channel_name)
    await text_channel.delete()

    channel_role = get_role_by_name(guild, role_name)
    await channel_role.delete()
