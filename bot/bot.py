import discord.ext.commands
from discord.ext.commands.context import Context

from . import handlers

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_scheduled_event_create(event: discord.ScheduledEvent):
    await handlers.handle_event_created(event)


@bot.event
async def on_scheduled_event_delete(event: discord.ScheduledEvent):
    await handlers.handle_event_deleted(event)


@bot.command(name="status")
async def status(context: Context):
    await handlers.handle_print_event_link(context=context)
