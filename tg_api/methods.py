from typing import Iterable, Callable, Union
from .files import Files
from .messages import Messages
from .types import Object

class Methods(Messages, Files):
    def __init__(self):
        super().__init__()
    async def build(self, default: Iterable, *args, **kwargs):
        params = {}
        for index in range(len(args)):
            params[default[index]] = args[index]
        for key in kwargs.keys():
            params[key] = kwargs[key]
        return params
    async def add_method(self, name: str, func: Callable):
        if not getattr(self, name, None):
            setattr(self, name, func)
        else:
            raise Exception("Method alredy exists")
    async def send(self, method: str, params: dict, return_type: Uninon[str, bool]="Custom"):
        r = await (await self.session.get(self.website+method, params=params)).json()
        if r['ok']:
            return Object(self, r['result'], return_type)
        else:
            raise Exception(f"[{r['error_code']}] {r['description']}")
