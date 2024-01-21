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

# requires: asyncurban

import logging

import asyncurban
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class UrbanDictionaryMod(loader.Module):
    """Define word meaning using UrbanDictionary."""
    strings = {"name": "Urban Dictionary",
               "provide_word": "<b>Provide a word(s) to define.</b>",
               "def_error": "<b>Couldn't find definition for that.</b>",
               "result": "<b>Text</b>: <code>{}</code>\n<b>Meaning</b>: <code>{}\n<b>Example</b>: <code>{}</code>"}

    def __init__(self):
        self.urban = asyncurban.UrbanDictionary()

    @loader.unrestricted
    @loader.ratelimit
    async def urbancmd(self, message):
        """Define word meaning. Usage:
            .urban <word(s)>"""

        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, self.strings("provide_word", message))

        try:
            definition = await self.urban.get_word(args)
        except asyncurban.WordNotFoundError:
            return await utils.answer(message, self.strings("def_error", message))
        result = self.strings("result", message).format(definition.word, definition.definition, definition.example)
        await utils.answer(message, result)
