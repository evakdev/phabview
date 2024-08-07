from phabview.adapters.base_adapter import BaseMessagingAdapter
from phabview.config import ROCKETCHAT_HOST, ROCKETCHAT_USER_ID, ROCKET_CHAT_USER_TOKEN, ROCKET_CHAT_BOT_ALIAS_NAME
import retry_async
from rocketchat_API.rocketchat import RocketChat


class RocketChatAdapter(BaseMessagingAdapter):
    def __init__(self):
        self.api = RocketChat(
            user_id=ROCKETCHAT_USER_ID,
            auth_token=ROCKET_CHAT_USER_TOKEN,
            server_url=ROCKETCHAT_HOST,
        )

    @retry_async.retry(is_async=True, tries=3)(delay=10, tries=10, backoff=2)
    async def send_to_user_dm(self, username: str, message: str):
        alias = ROCKET_CHAT_BOT_ALIAS_NAME or None
        response = self.api.chat_post_message(text=message, channel=f"@{username}", alias=alias)
        response.raise_for_status()
        return response.json()
