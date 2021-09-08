import os
import asyncio
from nio import (
    AsyncClient,
    RoomResolveAliasError,
)


def is_room_alias(room_id: str) -> bool:
    """Determine if room identifier is a room alias.
    Alias are of syntax: #somealias:someserver
    """
    if room_id and len(room_id) > 3 and room_id[0] == "#":
        return True
    else:
        return False


async def send(client, message):
    await client.login(os.environ["matrix_pass"])
    if is_room_alias(os.environ['matrix_room']):
        resp = await client.room_resolve_alias(room_id)
        if isinstance(resp, RoomResolveAliasError):
            print(f"room_resolve_alias failed with {resp}")
        room_id = resp.room_id
        logger.debug(
            f'Mapping room alias "{resp.room_alias}" to '
            f'room id "{resp.room_id}".'
        )
    try:
        await client.room_send(
                room_id=os.environ['matrix_room'],
                message_type="m.room.message",
                content={
                    "format": "org.matrix.custom.html",
                    "msgtype": os.environ['messagetype'],
                    "body": message,
                    "formatted_body": message,
                },
                ignore_unverified_devices=True,
        )
    except Exception as e:
        print("Message send failed. Sorry.")
        print("Here is the traceback.\n" + str(e))
    await client.close()


client = AsyncClient(os.environ['matrix_server'], os.environ['matrix_user'])
loop = asyncio.get_event_loop()
message = os.environ["message"]

#  uncomment these in case of python 3.5-3.6
#loop.run_until_complete(send(client, message))
#loop.close()

#  comment this in case of python 3.5-3.6
asyncio.run(send(client, message))
