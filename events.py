import discord
from bot import bot
from constants import TEXT_CHANNEL_SUFFIX
from utils import create_voice_text_channel, remove_voice_text_channel, get_role_by_name, format_text_channel_name


# Internal events


async def on_voice_channel_connect(member: discord.Member, channel: discord.VoiceChannel):
    guild: discord.Guild = member.guild
    text_channel_name = format_text_channel_name(f"${channel.name}${TEXT_CHANNEL_SUFFIX}")
    role_name = text_channel_name

    if not any(channel.name == text_channel_name for channel in guild.text_channels):
        await create_voice_text_channel(guild, role_name, channel.category)

    channel_role = get_role_by_name(guild, role_name)

    await member.add_roles(channel_role, atomic=True)


async def on_voice_channel_disconnect(member: discord.Member, channel: discord.VoiceChannel):
    guild: discord.Guild = member.guild
    text_channel_name = format_text_channel_name(f"${channel.name}${TEXT_CHANNEL_SUFFIX}")
    role_name = text_channel_name

    channel_role = get_role_by_name(guild, role_name)

    await member.remove_roles(channel_role)

    if len(channel.members) == 0:
        await remove_voice_text_channel(guild, text_channel_name, role_name)

# Discord api events


@bot.event
async def on_ready():
    print("Started")


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and after.channel is not None:
        await on_voice_channel_connect(member, after.channel)
    elif before.channel is not None and after.channel is None:
        await on_voice_channel_disconnect(member, before.channel)
