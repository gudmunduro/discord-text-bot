import discord

from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!tc ', intents=intents)
