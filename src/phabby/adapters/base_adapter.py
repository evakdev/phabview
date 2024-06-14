from phabby.utils import Singleton


class BaseMessagingAdapter:
    __metaclass__ = Singleton

    async def send(self, room: str, message: str):
        raise NotImplementedError
