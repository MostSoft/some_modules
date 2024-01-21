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
import random


@loader.tds
class YesNoMod(loader.Module):
    """Helps you make important life choices"""
    strings = {"name": "YesNo",
               "yes_words_cfg_doc": "Yes words",
               "no_words_cfg_doc": "No words"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "YES_WORDS", ["Yes", "Yup", "Absolutely", "Non't"], lambda m: self.strings("yes_words_cfg_doc", m),
            "NO_WORDS", ["No", "Nope", "Nah", "Yesn't"], lambda m: self.strings("no_words_cfg_doc", m))

    @loader.unrestricted
    async def yesnocmd(self, message):
        """Make a life choice"""
        yes = self.config["YES_WORDS"]
        no = self.config["NO_WORDS"]
        if random.getrandbits(1):
            response = random.choice(yes)
        else:
            response = random.choice(no)
        await utils.answer(message, response)
