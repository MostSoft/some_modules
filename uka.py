from asyncio import sleep
from .. import loader, utils

def register(cb):
	cb(ЗайобушкаMod())
	
class ЗайобушкаMod(loader.Module):
	strings = {'name': 'Fucker'}
		
	async def куcmd(self, message):
		""".ку <number> <reply>"""
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("<b>А кого зайобувати?</b>")
			return
		id = reply.sender_id
		args = utils.get_args(message)
		count = 50
		if args:
			if args[0].isdigit():
				if int(args[0]) < 0:
					count = 50
				else:
					count = int(args[0])
		txt = '<a href="tg://user?id={}">ку-ку :3</a>'.format(id)
		await message.delete()
		for _ in range(count):
			await sleep(0.3)
			msg = await message.client.send_message(message.to_id, txt)
			await sleep(0.3)
			await msg.delete()
