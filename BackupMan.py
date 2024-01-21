import ast
import io
from .. import loader, utils


@loader.tds
class BackupManMod(loader.Module):
    """BackupMan"""

    strings = {"name": "BackupMan"}

    async def client_ready(self, _, db):
        self._db = db

    @loader.owner
    async def restmcmd(self, m):
        "Install all modules from *.bkm file"
        reply = await m.get_reply_message()
        if not reply or not reply.file or reply.file.name.split(".")[-1] != "bkm":
            return await m.edit("<b>[BackupMan]</b> Reply to <code>*.bkm</code> file")
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO(await reply.download_media(bytes))
        valid, already_loaded = 0, 0
        for i in txt.read().decode("utf-8").split("\n"):
            if i not in modules:
                valid += 1
                modules.append(i)
            else:
                already_loaded += 1
        self._db.set("friendly-telegram.modules.loader", "loaded_modules", modules)
        await m.edit(
            f"<b>[BackupMan]</b>\n\n<i>Modules loaded:</i> <code>{valid}</code>\n<i>Already loaded:</i> <code>{already_loaded}</code>\n\n"
            + (
                "<b>> The userbot will automatically restart</b>"
                if valid != 0
                else "<b>> Nothing loaded</b>"
            )
        )
        if valid != 0:
            await self.allmodules.commands["restart"](await m.respond("_"))

    @loader.owner
    async def backmcmd(self, m):
        "Create a backup of modules in *.bkm file"
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO("\n".join(modules).encode("utf-8"))
        txt.name = f"BackupMan-{(await m.client.get_me()).id}.bkm"
        await m.client.send_file(
            m.to_id,
            txt,
            caption=f"<b>[BackupMan]</b> <i>Modules backup</i>\n<i>Modules:</i> <code>{len(modules)}</code>\n<i>To restore the backup, use the module:</i>\n<code>.dlmod https://d4n13l3k00.ru/modules/BackupMan.py</code>",
        )
        await m.delete()

    @loader.owner
    async def restncmd(self, m):
        "Install all notes from *.bkn file\n<f> - Replace existing notes"
        args: list or None = utils.get_args_raw(m)
        force = "f" in args.lower()
        reply = await m.get_reply_message()
        if not reply or not reply.file or reply.file.name.split(".")[-1] != "bkn":
            return await m.edit("<b>[BackupMan]</b> Reply to <code>*.bkn</code> file")
        notes = self._db.get("friendly-telegram.modules.notes", "notes", {})
        txt = io.BytesIO(await reply.download_media(bytes))
        valid, already_loaded = 0, 0
        for k, v in ast.literal_eval(txt.read().decode("utf-8")).items():
            if k not in notes or force:
                notes[k] = v
                valid += 1
            else:
                already_loaded += 1
        self._db.set("friendly-telegram.modules.notes", "notes", notes)
        await m.edit(
            f"<b>[BackupMan]</b>\n\n<i>Loaded/replaced notes:</i> <code>{valid}</code>\n<i>Already loaded:</i> <code>{already_loaded}</code>"
        )

    @loader.owner
    async def backncmd(self, m):
        "Create a backup of notes in *.bkn file"
        modules = self._db.get("friendly-telegram.modules.notes", "notes", {})
        txt = io.BytesIO(str(modules).encode("utf-8"))
        txt.name = f"BackupMan-{(await m.client.get_me()).id}.bkn"
        await m.client.send_file(
            m.to_id,
            txt,
            caption=f"<b>[BackupMan]</b> <i>Notes backup</i>\n<i>Notes:</i> <code>{len(modules)}</code>\n<i>To restore the backup, use the module:</i>\n<code>.dlmod https://d4n13l3k00.ru/modules/BackupMan.py</code>",
        )
        await m.delete()
