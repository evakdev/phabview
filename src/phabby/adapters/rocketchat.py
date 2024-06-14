from phabby.adapters.base_adapter import BaseMessagingAdapter
from phabby.config import ROCKETCHAT_HOST, ROCKETCHAT_PASSWORD, ROCKETCHAT_USERNAME
from retry import retry
from rocketchat_API.rocketchat import RocketChat


class RocketChatAdapter(BaseMessagingAdapter):
    def __init__(self):
        self.api = RocketChat(
            user=ROCKETCHAT_USERNAME,
            password=ROCKETCHAT_PASSWORD,
            server_url=ROCKETCHAT_HOST,
        )

    @retry(delay=10, tries=10, backoff=2)
    async def send(self, room: str, message: str):
        self.api.chat_post_message(room, message)
