from typing import Callable, Iterable
from inspect import iscoroutinefunction
from asyncio import create_task

class Filter:
    def __init__(self, callback: Callable, datas: [list, tuple]=None, args:Iterable=(), kwargs: dict={}):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if datas: self.datas = datas
    def __and__(self, other):
        return AndFilter(self, other)
    def __or__(self, other):
        return OrFilter(self, other)
    def __invert__(self):
        return InvertFiter(self)
    async def check(self, client, update):
        if iscoroutinefunction(self.callback):
            return (await self.callback(client, update, *self.args, **self.kwargs))
        else:
            return self.callback(client, update, *self.args, **self.kwargs)
class AndFilter(Filter):
    def __init__(self, base: Filter, other: Filter):
        self.base = base
        self.other = other
    async def check(self, *args, **kwargs):
        return  (await self.base.check(*args, **kwargs)) and (await self.other.check(*args, **kwarg))

class OrFilter(Filter):
    def __init__(self, base: Filter, other: Filter):
        self.base = base
        self.other = other
    async def check(self, *args, **kwargs):
        return (await self.base.check(*args, **kwargs)) or (await self.other.check(*args, **kwarg))

class InvertFiter(Filter):
    def __init__(self, filter: Filter):
        self.filter = filter
    async def check(self, *args, **kwargs):
        return not (await self.filter.check(*args, **kwargs))

class Filters:
    def __init__(self):
        self.__null__ = self.create(lambda *args, **kwargs: True)
    def create(self, func: Callable, datas: [list, tuple]=None, *args, **kwargs):
        obj = Filter(func, datas, args, kwargs)
        return getattr(obj, "datas", obj)
    def command(self, data: str, prefixes: [list, tuple]=["/"], startswith: bool=True):
        async def check_command(client, update):
            value = None
            if update.name == "Message":
                value = getattr(update, 'caption', update.text if hasattr(update, 'text') else None)
            elif update.name == "CallbackQuery":
                value = update.data
            if value and value[0] in prefixes:
                if startswith:
                    return value[1::].startswith(data)
                else:
                    return value[1::] == data
            return False
        return self.create(check_command)
    def users(self, users_list: [list, tuple]):
        async def check_users(client, update, users):
            value = getattr(update, "from_user", None)
            if value:
                return value.id in users or value.username in users
            return False
        return self.create(check_users, users_list, users_list)

filters = Filters()

