import io
from telethon import types
from .. import loader, utils

@loader.tds
class SaverMod(loader.Module):
    strings = {"name": "Saver"}

    async def client_ready(self, client, db):
        self.db = db

    @loader.owner
    async def savecmd(self, m: types.Message):
        ".save <reply> - download a self-destructing photo"
        reply = await m.get_reply_message()
        if not reply or not reply.media:
            return await m.edit("Error")
        await m.delete()
        new = io.BytesIO(await reply.download_media(bytes))
        new.name = reply.file.name
        await m.client.send_file("me", new)

    @loader.owner
    async def togglesavecmd(self, m: types.Message):
        "Toggle the auto-save mode for photos in PMs"
        new_val = not self.db.get("Saver", "state", False)
        self.db.set("Saver", "state", new_val)
        await utils.answer(m, f"<b>[Saver]</b> <pre>{new_val}</pre>")

    async def watcher(self, m: types.Message):
        if (
            m
            and m.media
            
            and self.db.get("Saver", "state", False)
        ):
            new = io.BytesIO(await m.download_media(bytes))
            new.name = m.file.name
            await m.client.send_file(
                "me",
                new,
                caption=f"<b>[Saver] Photo from</b> {f'@{m.sender.username}' if m.sender.username else m.sender.first_name} | <pre>{m.sender.id}</pre>",
            )
