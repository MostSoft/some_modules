from .. import loader, utils
from asyncio import sleep, gather


def register(cb):
    cb(SpamMod())

class SpamMod(loader.Module):
    """Spam module"""
    strings = {'name': 'Spam'}

    async def spamcmd(self, message):
        try:
            await message.delete()
            args = utils.get_args(message)
            count = int(args[0].strip())
            reply = await message.get_reply_message()
            if reply:
                if reply.media:
                    for _ in range(count):
                        await message.client.send_file(message.to_id, reply.media)
                    return
                else:
                    for _ in range(count):
                        await message.client.send_message(message.to_id, reply)
            else:
                message.message = " ".join(args[1:])
                for _ in range(count):
                    await gather(*[message.respond(message)])
        except: return await message.client.send_message(message.to_id, '.spam <number:int> <text/reply>')

    async def cspamcmd(self, message):
        """Spam with characters. Use .cspam <text/reply>."""
        await message.delete()
        reply = await message.get_reply_message()
        if reply:
            msg = reply.text
        else:
            msg = utils.get_args_raw(message)
        msg = msg.replace(' ', '')
        for m in msg:
            await message.respond(m)

    async def wspamcmd(self, message):
        """Spam with words. Use .wspam <text/reply>."""
        await message.delete()
        reply = await message.get_reply_message()
        if reply:
            msg = reply.text
        else:
            msg = utils.get_args_raw(message)
        msg = msg.split()
        for m in msg:
            await message.respond(m)

    async def delayspamcmd(self, message):
        """Spam with delay. Use .delayspam <time:int> <number:int> <text/reply>."""
        try:
            await message.delete()
            args = utils.get_args_raw(message)
            reply = await message.get_reply_message()
            time = int(args.split(' ', 2)[0])
            count = int(args.split(' ', 2)[1])
            if reply:
                if reply.media:
                    for _ in range(count):
                        await message.client.send_file(message.to_id, reply.media, reply_to=reply.id)
                        await sleep(time)
                else:
                    for _ in range(count):
                        await reply.reply(args.split(' ', 2)[2])
                        await sleep(time)
            else:
                spammsg = args.split(' ', 2)[2]
                for _ in range(count):
                    await message.respond(spammsg)
                    await sleep(time)
        except: return await message.client.send_message(message.to_id, '.delayspam <time:int> <number:int> <text/reply>')
