from .. import loader, utils

class DelmeMod(loader.Module):
    """Deletes all messages"""
    strings = {'name': 'DelMe'}

    @loader.sudo
    async def delmecmd(self, message):
        """Deletes all messages from you"""
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id + message.sender_id):
                await message.edit(f"<b>If you really want to do this, type:</b>\n<code>.delme {message.chat.id + message.sender_id}</code>")
                return
            await delete(chat, message, True)
        else:
            await message.edit("<b>Not deleting in PMs!</b>")

    @loader.sudo
    async def delmenowcmd(self, message):
        """Deletes all messages from you without asking"""
        chat = message.chat
        if chat:
            await delete(chat, message, False)
        else:
            await message.edit("<b>Not deleting in PMs!</b>")

async def delete(chat, message, now):
    if now:
        all_messages = (await message.client.get_messages(chat, from_user="me")).total
        await message.edit(f"<b>{all_messages} messages will be deleted!</b>")
    else:
        await message.delete()

    first_iteration = not now
    async for msg in message.client.iter_messages(chat, from_user="me"):
        if first_iteration:
            await msg.delete()
        else:
            first_iteration = False

    await message.delete() if now else "What?"
