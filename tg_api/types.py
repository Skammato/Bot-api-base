from typing import Callable, NewType, Iterable
from inspect import isfunction
from .messages import message_buonds
from json import dumps

class Buonds:
    def __init__(self):
        if self.name == "Message":
            self.bounds = message_buonds(self)

class Object(Buonds):
    def __init__(self, client, update, name=None, buonds=None):
        self.client = client
        self.name = name if name else self.__class__.__name__
        try:
            update["from_user"] = update["from"]
            del update["from"]
        except KeyError:
            pass
        for key in update.keys():
            if isinstance(update[key], dict):
                self.add(key, Object(self.client, update[key], key[0].upper()+key[1::]))
            else:
                self.add(key, update[key])
        super().__init__()
    def add(self, key: [str, int], value):
        if str(key) != "client":
            setattr(self, key, value)
    def default(obj) -> dict:
        final_dict = {"_":obj.name}
        value = None
        for key in obj.__dict__.keys():
            if str(key) not in ["client", "_", "name", "bounds"]:
                if isinstance(obj.__dict__[key], Object):
                    value = Object.default(obj.__dict__[key])
                else:
                    value = obj.__dict__[key]
                if not isfunction(value): final_dict[key] = value
        return final_dict
    def __str__(self) -> str:
        return dumps(Object.default(self), indent=4)

