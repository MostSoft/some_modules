import logging
from .. import loader, utils
import telethon

logger = logging.getLogger(__name__)


async def register(cb):
    cb(KeyboardSwitcherMod())


@loader.tds
class KeyboardSwitcherMod(loader.Module):
    strings = {
        "name": "KeyboardSwitcher"}

    async def switchcmd(self, message):
        EnKeys = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?"""
        UkKeys = """`йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,"""

        if message.is_reply:
            reply = await message.get_reply_message()
            text = reply.raw_text
            if not text:
                await message.edit('No text...')
                return
            change = str.maketrans(UkKeys + EnKeys, EnKeys + UkKeys)
            text = str.translate(text, change)

            if message.sender_id != reply.sender_id:
                await message.edit(text)
            else:
                await message.delete()
                await reply.edit(text)

        else:
            text = utils.get_args_raw(message)
            if not text:
                await message.edit('No text...')
                return
            change = str.maketrans(UkKeys + EnKeys, EnKeys + UkKeys)
            text = str.translate(text, change)
            await message.edit(text)
