import discord
from discord.ext.commands.context import Context

from . import WOMApi
from config import secret
import json
import os


async def handle_event_created(event: discord.ScheduledEvent) -> None:
    if not event.name.startswith("SOTW:"):
        return

    response = WOMApi.create(
        title=event.name,
        metric=event.description,
        startsAt=event.start_time,
        endsAt=event.end_time,
        groupId=secret.GROUP_ID,
        groupVerificationCode=secret.VERIFICATION_CODE
    )
    status_code = response.status_code
    channel = event.guild.get_channel(secret.CHANNEL_ID)

    if status_code == 201:
        sotw_content = json.loads(response.content.decode())
        sotw_id = sotw_content["competition"]["id"]
        save_sotw(sotw_id)
        await channel.send(f"Created SOTW: https://wiseoldman.net/competitions/{sotw_id}")
    else:
        await channel.send("Could not create SOTW :(")
        await event.delete(reason="Could not create SOTW, try to create it again.")


async def handle_event_deleted(event: discord.ScheduledEvent) -> None:
    if not event.name.startswith("SOTW:"):
        return

    sotw_id = load_sotw_id()
    response = WOMApi.delete(sotw_id, secret.VERIFICATION_CODE)
    status_code = response.status_code

    if status_code != 200:
        channel = event.guild.get_channel(secret.CHANNEL_ID)
        await channel.send("Could not delete SOTW :(")


async def handle_print_event_link(context: Context) -> None:
    if context.channel.id != secret.CHANNEL_ID:
        return

    sotw_id = load_sotw_id()
    if sotw_id is None:
        message = "No SOTW is planned/in progress."
    else:
        message = f"Current SOTW: https://wiseoldman.net/competitions/{sotw_id}"
    await context.send(message)


def save_sotw(sotw_id: int, file_name: str = 'current_sotw.json') -> None:
    with open(secret.SOTW_PATH + file_name, 'w') as f:
        json.dump(sotw_id, f)


def load_sotw_id(file_name: str = 'current_sotw.json') -> int | None:
    try:
        with open(secret.SOTW_PATH + file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def delete_sotw(file_name: str = 'current_sotw.json') -> None:
    os.remove(secret.SOTW_PATH + file_name)
