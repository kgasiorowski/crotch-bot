import discord

import WOMApi
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

    if status_code == 201:
        sotw_content = json.loads(response.content.decode())
        sotw_id = sotw_content["competition"]["id"]
        save_sotw(sotw_id)
    else:
        channel = event.guild.get_channel(secret.CHANNEL_ID)
        await channel.send("Could not create SOTW")
        await event.delete(reason="Could not create SOTW, try to create it again.")


def handle_event_deleted(event: discord.ScheduledEvent) -> None:
    if not event.name.startswith("SOTW:"):
        return


def save_sotw(sotw_id: int, file_name: str = 'current_sotw.json'):
    with open(secret.SOTW_PATH + file_name, 'w') as f:
        json.dump(sotw_id, f)


def load_sotw_id(file_name: str = 'current_sotw.json'):
    try:
        with open(secret.SOTW_PATH + file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def delete_sotw(file_name: str = 'current_sotw.json'):
    os.remove(secret.SOTW_PATH + file_name)
