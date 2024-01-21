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

# requires: gtts hachoir

from gtts import gTTS

from io import BytesIO

from .. import loader, utils


@loader.tds
class TTSMod(loader.Module):
    strings = {"name": "Text to speech",
               "tts_lang_cfg": "Set your language code for the TTS here.",
               "tts_needs_text": "<code>I need some text to convert to speech!</code>"}

    def __init__(self):
        self.config = loader.ModuleConfig("TTS_LANG", "en", lambda m: self.strings("tts_lang_cfg", m))

    @loader.unrestricted
    @loader.ratelimit
    async def ttscmd(self, message):
        """Convert text to speech with Google APIs"""
        text = utils.get_args_raw(message.message)
        if len(text) == 0:
            if message.is_reply:
                text = (await message.get_reply_message()).message
            else:
                await utils.answer(message, self.strings("tts_needs_text", message))
                return

        tts = await utils.run_sync(gTTS, text, lang=self.config["TTS_LANG"])
        voice = BytesIO()
        await utils.run_sync(tts.write_to_fp, voice)
        voice.seek(0)
        voice.name = "voice.mp3"

        await utils.answer(message, voice, voice_note=True)
