# -*- coding: utf-8 -*-

#   Friendly Telegram (telegram userbot)
#   Copyright (C) 2018-2020 @DneZyeK | sub to @KeyZenD

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    EnKeys = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""
    UkKeys = """`йцукенгшщзхїфівапролджєячсмитьбю.ХЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,"""  # Українські букви

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
