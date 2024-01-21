#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging
import asyncio

logger = logging.getLogger(__name__)


@loader.tds
class QuickTypeMod(loader.Module):
    """Deletes your message after a timeout"""
    strings = {"name": "Quick Typer",
               "need_something": "U wot? I need something to type",
               "lazy_af": "Go type it urself m8",
               "nice_number": "Nice number bro"}

    async def quicktypecmd(self, message):
        """.quicktype <timeout> <message>"""
        args = utils.get_args(message)
        logger.debug(args)
        if len(args) == 0:
            await utils.answer(message, self.strings("need_something", message))
            return
        if len(args) == 1:
            await utils.answer(message, self.strings("lazy_af", message))
            return
        t = args[0]
        mess = " ".join(args[1:])
        try:
            t = float(t)
        except ValueError:
            await utils.answer(message, self.strings("nice_number", message))
            return
        await utils.answer(message, mess)
        await asyncio.sleep(t)
        await message.delete()
