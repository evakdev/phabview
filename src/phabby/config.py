import os

from dotenv import load_dotenv

load_dotenv()

# Generic
NOTIFY_ANY_USER = os.getenv("NOTIFY_ANY_USER", "False") == "True"
NOTIFIABLE_USERS = os.getenv("NOTIFIABLE_USERS", "").split(",")
MESSAGING_ADAPTER = os.getenv("MESSAGING_ADAPTER", "rocketchat")
# Currently only rocketchat is available.


# Phabricator
PHABRICATOR_HOST = f'{os.getenv("PHABRICATOR_HOST", "")}/api/'
PHABRICATOR_USERNAME = os.getenv("PHABRICATOR_USERNAME", "")
PHABRICATOR_TOKEN = os.getenv("PHABRICATOR_TOKEN", "")
PHABRICATOR_WEBHOOK_HMAC_KEY = os.getenv("PHABRICATOR_WEBHOOK_HMAC_KEY", "")
PHABRICATOR_REVISION_TYPE_NAME = "DREV"
PHABRICATOR_HMAC_HEADER_NAME = "x-phabricator-webhook-signature"

# Rocketchat
ROCKETCHAT_HOST = os.getenv("ROCKETCHAT_HOST", "")
ROCKETCHAT_USERNAME = os.getenv("ROCKETCHAT_USERNAME", "")
ROCKETCHAT_PASSWORD = os.getenv("ROCKETCHAT_PASSWORD", "")
