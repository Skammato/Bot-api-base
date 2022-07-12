import asyncio
from urllib.request import urlretrieve
from inspect import iscoroutinefunction
from typing import Callable

class Files:
    async def getFile(self, *args, **kwargs):
        default = ["file_id"]
        params = await self.build(default, *args, **kwargs)
        return (await self.send("getFile", params, "File"))
    async def download_media(self, file_id: str, file_name: str="{unique_id}.{ext}", report_hook: Callable=None, report_hook_args: [tuple, list]=()):
        obj = await self.getFile(file_id) #get url file, from telegram servers, to download
        if hasattr(obj, 'file_path'):
            #check if there is the file_path to download
            def ReportHook(count, block_size, total_size):
                if (count * block_size) < total_size:
                    #if download is not completed will call the hook
                    if iscoroutinefunction(report_hook):
                        #async in sync
                        asyncio.create_task(report_hook(count * block_size, total_size, *report_hook_args))
                    else:
                        report_hook(count * block_size, total_size, *report_hook_args)
            #download and return the file name
            return urlretrieve(f"https://api.telegram.org/file/bot{self.token}/{obj.file_path}", file_name.format(unique_id=obj.file_unique_id, ext=obj.file_path.split(".")[1]), reporthook=ReportHook if report_hook else None)[0]
        else:
            raise Exception("[400] File_id is invalid or is expired")
