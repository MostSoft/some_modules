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
import urllib

logger = logging.getLogger(__name__)


@loader.tds
class LMGTFYMod(loader.Module):
    """Let me Google that for you, coz you too lazy to do that yourself."""
    strings = {"name": "LetMeGoogleThatForYou",
               "result": "<b>Here you go, help yourself.</b>\n<a href='{}'>{}</a>",
               "default": "How to use Google?"}

    @loader.unrestricted
    async def lmgtfycmd(self, message):
        """Use in reply to another message or as .lmgtfy <text>"""
        text = utils.get_args_raw(message)
        if not text:
            if message.is_reply:
                text = (await message.get_reply_message()).message
            else:
                text = self.strings("default", message)
        query_encoded = urllib.parse.quote_plus(text)
        lmgtfy_url = "http://lmgtfy.com/?s=g&iie=1&q={}".format(query_encoded)
        await utils.answer(message,
                           self.strings("result", message).format(utils.escape_html(lmgtfy_url),
                                                                  utils.escape_html(text)))
