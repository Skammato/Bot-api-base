from inspect import iscoroutinefunction
from .filters import Filter, filters
from typing import Callable, Iterable

class handlers(object):
    def __init__(self):
        self.MessageHandler = MessageHandler
        self.CallbackQueryHandler = CallbackQueryHandler

class Handler:
    def __init__(self, callback: Callable, filters: Filter=filters.__null__, args: Iterable=()):
        callback.is_async = iscoroutinefunction(callback)
        self.callback = callback
        self.filter = filters
        self.args = args
    def __str__(self):
        dict = {
        "_":type(self),
        "callback":self.callback.__name__,
        "filters":self.filter,
        "callback_args":self.args
        }
        return str(dict)

class MessageHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class CallbackQueryHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Decorators(object):
    def on_message(self, *args, **kwargs):
        return self.create_decorator(MessageHandler, *args, **kwargs)
    def on_callback_query(self, *args, **kwargs):
        return self.create_decorator(CallbackQueryHandler, *args, **kwargs)
    def create_decorator(self, TypeHandler, *args, **kwargs):
        def wrapper(callback: Callable):
            return self.add_handler(TypeHandler(callback, *args, **kwargs))
        return wrapper
