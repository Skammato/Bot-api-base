from asyncio import get_event_loop, create_task, sleep, run
from aiohttp import ClientSession
from .client import Client
from .handlers import handlers
from .filters import filters

__version__ =  "0.0.2"
TelegramClient = Client
filters = filters

def idle(self, *sessions):
    loop = get_event_loop()
    async def main():
        s = ClientSession()
        for client in sessions:
            await client.start(False, s)
        try:
            while True:
                for client in sessions:
                    if not client.no_updates:
                        await client.get_updates()
        except KeyboardInterrupt:
            for session in sessions:
                print(u"\u001b[32m[{}] stopped!\u001b[0m".format(session.session_name))
            loop.stop()
            run(s.close())
    loop.run_until_complete(main())
