import enum

from phabby.adapters.rocketchat import RocketChatAdapter
from phabby.config import MESSAGING_ADAPTER


class MessagingAdapterEnum(enum.Enum):
    rocketchat = "rocketchat"


class AdapterFactory:
    def get_adapter(self):
        if MessagingAdapterEnum.rocketchat == MESSAGING_ADAPTER:
            return RocketChatAdapter()
        raise NotImplementedError(f"Messaging Adapter named {MESSAGING_ADAPTER} does not exist.")
