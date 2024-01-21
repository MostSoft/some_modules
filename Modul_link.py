import io, inspect
from .. import loader, utils

@loader.tds
class ModulesLinkMod(loader.Module):
    """Module Link"""
    strings = {'name': 'ModulesLink'}

    async def mlcmd(self, message):
        """Get a link to the module"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit('No arguments provided.')

        await message.edit('Searching...')

        try:
            module_name = ' '.join([x.strings["name"] for x in self.allmodules.modules if args.lower() == x.strings["name"].lower()])
            module_obj = next(filter(lambda x: args.lower() == x.strings["name"].lower(), self.allmodules.modules))
            module_source = inspect.getmodule(module_obj)

            link = str(module_source).split('(')[1].split(')')[0]
            if "http" not in link:
                text = f"Module {module_name}:"
            else:
                text = f"<a href=\"{link}\">URL</a> for 🇺🇦{module_name}: <code>{link}</code>"

            source_code = io.BytesIO(module_source.__loader__.data)
            source_code.name = module_name + ".py"
            source_code.seek(0)

            await message.respond(text, file=source_code)
            await message.delete()
        except:
            return await message.edit("Try entering the module name in quotes.")
