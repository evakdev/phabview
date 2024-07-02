from phabview.adapters.base_adapter import BaseMessagingAdapter
from phabview.config import ROCKETCHAT_HOST, ROCKETCHAT_USER_ID, ROCKET_CHAT_USER_TOKEN
from retry import retry
from rocketchat_API.rocketchat import RocketChat


class RocketChatAdapter(BaseMessagingAdapter):
    def __init__(self):
        self.api = RocketChat(
            user_id=ROCKETCHAT_USER_ID,
            auth_token=ROCKET_CHAT_USER_TOKEN,
            server_url=ROCKETCHAT_HOST,
        )

    @retry(delay=10, tries=10, backoff=2)
    def send_to_user_dm(self, username: str, message: str):
        response = self.api.chat_post_message(text=message, channel=f"@{username}").json()
        response.raise_for_status()
