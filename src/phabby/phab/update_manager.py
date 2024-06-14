from phabby.notification_builder import NotificationBuilder
from phabby.phab.adapter import PhabricatorAdapter
from phabby.phab.models import Revision, Update, UpdateTypeEnum

a = {
    "data": [
        {
            "id": 17,
            "phid": "PHID-XACT-HWBH-flt3laqvlpodgkm",
            "type": None,
            "authorPHID": "PHID-USER-ooluj6mheatikw2idi6l",
            "objectPHID": "PHID-HWBH-fuvlunlvwirxklq364py",
            "dateCreated": 1718291149,
            "dateModified": 1718291149,
            "groupID": "sarogp6iaozx7kqxjpr6e6punwip46dq",
            "comments": [],
            "fields": {},
        },
    ],
    "cursor": {"limit": 100, "after": None, "before": None},
}
b = {
    "data": [
        {
            "id": 13509,
            "phid": "PHID-XACT-DREV-mexevxrqgvrcci2",
            "type": None,
            "authorPHID": "PHID-USER-ooluj6mheatikw2idi6l",
            "objectPHID": "PHID-DREV-ntxkd5nonzb2w2al72tz",
            "dateCreated": 1718291182,
            "dateModified": 1718291182,
            "groupID": "bgboq6xcourgtei53rdsk4gwf533vrfw",
            "comments": [],
            "fields": {},
        },
    ],
    "cursor": {"limit": 100, "after": None, "before": None},
}


class UpdateManager:
    def __init__(self):
        self.phabricator_adapter = PhabricatorAdapter()
        self.notification_builder = NotificationBuilder()

    def get_update(self, changed_object: dict, transactions: list[str]):
        raw_update_list = PhabricatorAdapter().get_transactions(
            changed_object["phid"], transaction_phids=transactions,
        )
        generic_update = None
        for raw_update in raw_update_list:
            update_type = raw_update["type"]
            if update_type is None:
                update_type = UpdateTypeEnum.generic.value
            if update_type not in UpdateTypeEnum.list():
                continue
            raw_revision = self.phabricator_adapter.get_revision(
                raw_update["objectPHID"],
            )
            revision = Revision(raw_revision)

            update = Update(
                update_type=update_type,
                change_user=raw_update["authorPHID"],
                revision=revision,
            )
            if update_type != UpdateTypeEnum.generic.value:
                # If update has type, it has priority over unknowns.
                return update
        # We only return a generic update if no named update was found
        return generic_update
    def get_to_be_notified_usernames(self, update: Update) -> list[str]:
        usernames = []
        for phid in update.to_be_notified_users:
            usernames.append(self.phabricator_adapter.get_user_username(phid))

        return usernames

    def create_notifs(self, update: Update):
        notifiable_user_names = self.get_to_be_notified_usernames(update)
        change_user_name=self.phabricator_adapter.get_user_username(update.change_user)
        notifications = []
        for user in notifiable_user_names:
            notification = {"user": user}
            match update.update_type:
                case UpdateTypeEnum.create.value:
                    notification["text"] = self.notification_builder.new_review_request(
                        change_user_name, update.revision.link,
                    )
                case UpdateTypeEnum.update.value:
                    notification["text"] = (
                        self.notification_builder.new_update_review_request(
                            change_user_name, update.revision.link,
                        )
                    )
                case UpdateTypeEnum.comment.value:
                    if update.change_user == update.revision.owner:
                        # Owner responded to a comment
                        notification["text"] = (
                            self.notification_builder.new_comment_by_owner(
                                change_user_name, update.revision.link,
                            )
                        )
                    else:
                        # it was probably a review:
                        notification["text"] = (
                            self.notification_builder.new_incoming_review(
                                change_user_name, update.revision.link,
                            )
                        )
                case UpdateTypeEnum.generic.value:
                    notification["text"] = self.notification_builder.new_generic_update(
                        change_user_name, update.revision.link,
                    )
            notifications.append(notification)
        return notifications
