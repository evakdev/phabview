from phabview.utils import Singleton


class BaseMessagingAdapter:
    __metaclass__ = Singleton

    async def send_to_user_dm(self, username: str, message: str):
        raise NotImplementedError
