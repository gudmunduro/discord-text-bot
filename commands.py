import discord

from bot import bot
from discord.ext import commands
from datetime import datetime
from constants import BOT_NAME, INSUFFICIENT_PERMISSION_MESSAGE
from utils import get_channel_tag_role, remove_voice_text_channel, has_commands_permission, get_role_by_name


@bot.command(name="da")
async def delete_all(ctx: commands.Context):
    if not await has_commands_permission(ctx.message.author):
        await ctx.send(INSUFFICIENT_PERMISSION_MESSAGE)
        return

    tag_role = await get_channel_tag_role(ctx.guild)

    for channel in ctx.guild.channels:
        if tag_role in channel.overwrites:
            await remove_voice_text_channel(ctx.guild, channel.name, channel.name)
            if channel.category is not None and len(channel.category.channels) == 0:
                await channel.category.delete()

    await tag_role.delete()
    await ctx.send("All channels and roles deleted")


@bot.command(name="dd")
async def delete_duplicates(ctx: commands.Context):
    if not await has_commands_permission(ctx.message.author):
        await ctx.send(INSUFFICIENT_PERMISSION_MESSAGE)
        return

    tag_role = await get_channel_tag_role(ctx.guild)
    found_names = set()

    for channel in ctx.guild.channels:
        if tag_role in channel.overwrites:
            if channel.name in found_names:
                await channel.delete()
                if channel.category is not None and len(channel.category.channels) == 0:
                    await channel.category.delete()
            else:
                found_names.add(channel.name)

    await tag_role.delete()
    await ctx.send("All duplicate channels deleted")


@bot.command(name="listall")
async def list_all(ctx: commands.Context):
    if not await has_commands_permission(ctx.message.author):
        await ctx.send(INSUFFICIENT_PERMISSION_MESSAGE)
        return

    tag_role = await get_channel_tag_role(ctx.guild)

    channel_names = [channel.name for channel in ctx.guild.channels
                     if tag_role in channel.overwrites]
    channel_list_text = "\n".join(channel_names)

    await ctx.send(f"Channels created by bot:\n{channel_list_text}")


@bot.command(name="resetroles")
async def reset_roles(ctx: commands.Context):
    if not await has_commands_permission(ctx.message.author):
        await ctx.send(INSUFFICIENT_PERMISSION_MESSAGE)
        return

    tag_role = await get_channel_tag_role(ctx.guild)

    channel_names = [channel.name for channel in ctx.guild.channels
                     if tag_role in channel.overwrites]
    roles = [get_role_by_name(ctx.guild, name) for name in channel_names]

    async for member in ctx.guild.fetch_members(limit=None):
        await member.remove_roles(*roles)

    await ctx.send("All roles reset")


@bot.command(name="clearafter")
async def clear_messages(ctx: commands.Context, after_date: str, after_time: str):
    if not await has_commands_permission(ctx.message.author):
        await ctx.send(INSUFFICIENT_PERMISSION_MESSAGE)
        return

    tag_role = await get_channel_tag_role(ctx.guild)
    if tag_role not in ctx.channel.overwrites:
        await ctx.send(f"Channel was not created by {BOT_NAME}")
        return

    after_datetime = datetime.strptime(f"{after_date} {after_time}", '%d-%m-%Y %H:%M')
    if after_date is None:
        await ctx.send("Invalid date")
        return

    delete_queue = [message async for message in ctx.channel.history(limit=200)
                    if message.created_at > after_datetime]
    await ctx.channel.delete_messages(delete_queue)

    await ctx.send(f"All messages created after {after_date} {after_time} deleted")
