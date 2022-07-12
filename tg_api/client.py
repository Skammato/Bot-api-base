import aiohttp, json, asyncio
from traceback import format_exc
from .handlers import Decorators, MessageHandler, CallbackQueryHandler
from typing import Iterable, NewType
from .methods import Methods
from .types import Object

class Client(Decorators, Methods):
    def __init__(self, session: str, token: str, website: str="https://api.telegram.org/bot", no_updates: bool=False, allowed_updates: list=["message", "callback_query"]):
        """Create the new session:
        session = session name
        token = api token of the bot. Created from t.me/botfather
        website = telegram api, default, or your webhook
        """
        self.session_name = session
        self.token = token
        self.website = website+token+"/"
        self.allowed_updates = allowed_updates
        self.handlers = {
        "MESSAGE_HANDLER":[],
        "CALLBACK_QUERY_HANDLER":[]
        }
        self.no_updates = no_updates
        self.loop = asyncio.new_event_loop()
        super().__init__()
    async def generator(self, iter: Iterable):
        for i in iter:
            yield i
    def add_handler(self, handler):
        if isinstance(handler, MessageHandler):
            return self.handlers["MESSAGE_HANDLER"].append(handler)
        elif isinstance(handler, CallbackQueryHandler):
            return self.handlers["CALLBACK_QUERY_HANDLER"].append(handler)
    async def get_handler(self, string: str):
        return self.handlers[
        {"message":"MESSAGE_HANDLER",
        "callback_query":"CALLBACK_QUERY_HANDLER"
        }[string]
        ]
    async def set_session(self, s: aiohttp.ClientSession=None):
        if not s: s = aiohttp.ClientSession()
        self.session = s
    async def get_updates(self):
        """Get updates from telegram"""
        #response = requests.get(self.website+"getupdates", params={"offset":-1, "allowed_updates":json.dumps(self.allowed_updates)}).json()
        request = await self.session.get(self.website+"getupdates", params={"offset":-1, "allowed_updates":json.dumps(self.allowed_updates)})
        response = await request.json()
        if response["ok"] == False:
            raise Exception(f"[{response['error_code']}] {response['description']}")
        async for update in self.generator(response["result"]):
            kind = list(update)[1]
            async for handler in self.generator((await self.get_handler(kind))):
                obj = Object(self, update[kind], kind[0].upper()+kind[1::])
                if (await handler.filter.check(self, obj)):
                    if handler.callback.is_async:
                        try:
                            await handler.callback(self, obj, *handler.args)
                        except Exception as e:
                            format_exc()
                await self.confirm_update(update['update_id'])
    async def confirm_update(self, update_id: int):
        r = await (await self.session.get(self.website+"getupdates", params={"offset":update_id+1, "allowed_updates":json.dumps(self.allowed_updates)})).json()
        if r['ok'] == True and len(r['result']) == 0:
            return True
        else:
            raise Exception("Impossible to confirm the update")
    def start(self, loop: bool=True, s: aiohttp.ClientSession=None):
        """If the loop == True Run in loop get_updates. Else do nothing, because idle will starts the loop (Obv if you call it)"""
        try:
            async def main(loop):
                await self.set_session(s)
                while not self.no_updates:
                    await self.get_updates()
            print(u"\u001b[33m[{}] started!\u001b[0m".format(self.session_name))
            self.loop.run_until_complete(main(loop)) if loop else self.loop.run_until_complete(self.set_session())
        except KeyboardInterrupt:
            print(u"\u001b[32m[{}] stopped!\u001b[0m".format(self.session_name))
            self.loop.stop()
            asyncio.run(self.session.close())
