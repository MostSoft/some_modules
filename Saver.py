import io
import os
from datetime import datetime
from telethon import types
from .. import loader, utils

@loader.tds
class SaverMod(loader.Module):
    strings = {"name": "Saver"}
    
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()
    
    def _get_filename(self, m: types.Message):
        if hasattr(m.media, 'photo'):
            ext = '.jpg'
        elif hasattr(m.media, 'document'):
            doc = m.media.document
            mime_type = doc.mime_type
            if 'video' in mime_type:
                ext = '.mp4'
            elif 'image' in mime_type:
                ext = '.jpg'
            else:
                ext = ''
        else:
            ext = ''
        
        # Формування назви з датою та розширенням
        date_str = m.date.strftime("%Y-%m-%d_%H-%M-%S")
        return f"{date_str}{ext}"
    
    @loader.owner
    async def ляcmd(self, m: types.Message):
        ".ля <reply> - download a self-destructing media"
        reply = await m.get_reply_message()
        if not reply or not reply.media:
            # return await m.edit("Error: No media found in replied message")
            return
        
        if reply.media.ttl_seconds is None:
            # return await m.edit("Error: This media does not have a self-destruct timer")
            return
        
        try:
            await m.delete()
            media = await reply.download_media(bytes)
            new = io.BytesIO(media)
            new.name = self._get_filename(reply)
            
            await self.client.send_file(
                "me", 
                new,
                caption=f"<b>[Saver]</b> Saved self-destructing media (TTL: {reply.media.ttl_seconds} sec)"
            )
        except Exception as e:
            await m.edit(f"Error saving media: {str(e)}")
    
    @loader.owner
    async def togglesavecmd(self, m: types.Message):
        "Toggle the auto-save mode for self-destructing media in PMs"
        new_val = not self.db.get("Saver", "state", False)
        self.db.set("Saver", "state", new_val)
        await utils.answer(m, f"<b>[Saver]</b> Auto-save mode: <pre>{new_val}</pre>")
    
    async def watcher(self, m: types.Message):
        if (
            m 
            and m.media 
            and self.db.get("Saver", "state", False)
            and m.is_private
            and m.media.ttl_seconds is not None
            and m.peer_id.user_id != self.me.id
        ):
            try:
                media = await m.download_media(bytes)
                new = io.BytesIO(media)
                new.name = self._get_filename(m)
                
                await self.client.send_file(
                    "me",
                    new,
                    caption=f"<b>[Saver] Media from</b> {f'@{m.sender.username}' if m.sender.username else m.sender.first_name} | <pre>{m.sender.id}</pre> (TTL: {'1 time use' if m.media.ttl_seconds > 30 else f'{m.media.ttl_seconds} sec'})",
                )
            except Exception as e:
                print(f"Error in auto-save: {str(e)}")
