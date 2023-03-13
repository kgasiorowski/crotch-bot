import discord.ext.commands

from config import secret
from . import handlers

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_scheduled_event_create(event: discord.ScheduledEvent):
    await handlers.handle_event_created(event)


@bot.event
async def on_scheduled_event_delete(event: discord.ScheduledEvent):
    handlers.handle_event_deleted(event)
