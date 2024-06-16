import enum

from phabview.adapters.rocketchat import RocketChatAdapter
from phabview.config import MESSAGING_ADAPTER


class MessagingAdapterEnum(enum.Enum):
    rocketchat = "rocketchat"


class AdapterFactory:
    def get_adapter(self):
        if MESSAGING_ADAPTER == MessagingAdapterEnum.rocketchat.value:
            return RocketChatAdapter()
        raise NotImplementedError(f"Messaging Adapter named {MESSAGING_ADAPTER} does not exist.")
