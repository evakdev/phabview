import hashlib
import hmac
from phabview.config import (
    PHABRICATOR_REVISION_TYPE_NAME,
    PHABRICATOR_WEBHOOK_HMAC_KEY,
    NOTIFY_ANY_USER,
    NOTIFIABLE_USERS,
)
from phabview.adapters.adapter_factory import AdapterFactory
from phabview.phab.update_manager import UpdateManager


class PhabView:
    def verify_hmac(self, request_data: bytes, hmac_header: str):
        hmac_object = hmac.new(
            key=bytes(PHABRICATOR_WEBHOOK_HMAC_KEY, "utf-8"),
            msg=request_data,
            digestmod=hashlib.sha256,
        )
        signature = hmac_object.hexdigest()
        if hmac_header != signature:
            raise Exception

    async def handle(self, webhook_data: dict):
        changed_object = webhook_data["object"]

        if changed_object["type"] != PHABRICATOR_REVISION_TYPE_NAME:
            print(f"Invalid webhook type: {changed_object['type']}")
            return
        print(f"webhook_data:\n{webhook_data}")
        raw_transactions = self._get_raw_transactions(webhook_data)
        phabricator_update_manager = UpdateManager()
        update = phabricator_update_manager.get_update(changed_object, raw_transactions)
        if not update:
            return

        notifications = phabricator_update_manager.create_notifs(update)
        await self.send_notifications(notifications)

    async def send_notifications(self, notifications):
        messaging_adapter = AdapterFactory().get_adapter()

        if NOTIFY_ANY_USER:
            for notification in notifications:
                print(f'to {notification["username"]}: {notification["text"]}')
                await messaging_adapter.send_to_user_dm(notification["username"], notification["text"])
            return
        for notification in notifications:
            if notification["username"] in NOTIFIABLE_USERS:
                print(f'to {notification["username"]}: {notification["text"]}')
                await messaging_adapter.send_to_user_dm(notification["username"], notification["text"])

    def _get_raw_transactions(self, webhook_data):
        transactions = []
        for transaction in webhook_data["transactions"]:
            transactions.extend(transaction.values())
        return transactions
