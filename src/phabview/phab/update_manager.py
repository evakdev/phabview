from phabview.notification_builder import NotificationBuilder
from phabview.phab.adapter import PhabricatorAdapter
from phabview.phab.models import Revision, Update, UpdateTypeEnum, Reviewer


class UpdateManager:
    def __init__(self):
        self.phabricator_adapter = PhabricatorAdapter()
        self.notification_builder = NotificationBuilder()

    def get_update(self, changed_object: dict, transactions: list[str]):
        raw_update_list = PhabricatorAdapter().get_transactions(changed_object["phid"], transaction_phids=transactions)
        # Get first update, first. This helps avoid sending update notif when there was a create first
        raw_update_list.reverse()
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
            self.replace_groups_with_members(revision)
            update = Update(
                update_type=update_type,
                change_user=raw_update["authorPHID"],
                revision=revision,
            )
            if update_type == UpdateTypeEnum.generic.value:
                generic_update = update
            else:
                # If update has type, it has priority over unknowns.
                return update

        # We only return a generic update if no named update was found
        return generic_update

    def replace_groups_with_members(self, revision: Revision):
        subscribers = []
        for phid in revision.subscribers:
            if phid.startswith("PHID-USER"):
                subscribers.append(phid)
            elif phid.startswith("PHID-PROJ"):
                members = self.phabricator_adapter.get_project_members(phid)
                subscribers.extend(members)
        revision.subscribers = list(set(subscribers))
        group_reviewers = []
        individual_reviewers = {}
        for reviewer in revision.reviewers:
            if reviewer.is_group:
                group_reviewers.append(reviewer)
            else:
                individual_reviewers[reviewer.phid] = reviewer
        for group in group_reviewers:
            members = self.phabricator_adapter.get_project_members(group.phid)
            for member in members:
                if individual_reviewers.get(member):
                    continue
                individual_reviewers[member] = Reviewer(phid=member, status=group.status)
        revision.reviewers = list(individual_reviewers.values())

    def get_to_be_notified_users(self, update: Update) -> dict:
        # this list is in order. just in case there is a role overlap, we will notify for
        # the most important role. subscriber < reviewer < owner

        to_be_notified_users = {}
        for user in update.revision.subscribers:
            to_be_notified_users[user] = "subscriber"
        for user in update.to_be_notified_reviewers:
            to_be_notified_users[user] = "reviewer"
        to_be_notified_users[update.revision.owner] = "owner"

        to_be_notified_users.pop(update.change_user, None)
        return to_be_notified_users

    def create_notifs(self, update: Update):
        users = self.get_to_be_notified_users(update)
        change_username = self.phabricator_adapter.get_user_username(update.change_user)
        notifications = []
        if not change_username:  # It's Harbormaster
            return notifications
        for user_phid, role in users.items():
            username = self.phabricator_adapter.get_user_username(user_phid)
            notification = {"username": username}
            is_subscriber = role == "subscriber"
            match update.update_type:
                case UpdateTypeEnum.create.value:
                    notification["text"] = self.notification_builder.new_review_request(
                        creator_user=change_username, revision_link=update.revision.link, is_subscriber=is_subscriber
                    )
                case UpdateTypeEnum.update.value:
                    notification["text"] = self.notification_builder.new_update_review_request(
                        creator_user=change_username, revision_link=update.revision.link, is_subscriber=is_subscriber
                    )
                case UpdateTypeEnum.comment.value | UpdateTypeEnum.inline.value:
                    if update.change_user == update.revision.owner:
                        # Owner responded to a comment
                        notification["text"] = self.notification_builder.new_comment_by_owner(
                            creator_user=change_username,
                            revision_link=update.revision.link,
                            is_subscriber=is_subscriber,
                        )
                    else:
                        # it was probably a review
                        if role == "owner":
                            notification["text"] = self.notification_builder.new_incoming_review_for_owner(
                                creator_user=change_username, revision_link=update.revision.link
                            )
                        else:
                            notification["text"] = self.notification_builder.new_incoming_review_generic(
                                creator_user=change_username,
                                revision_link=update.revision.link,
                                is_subscriber=is_subscriber,
                            )
                case UpdateTypeEnum.generic.value:
                    notification["text"] = self.notification_builder.new_generic_update(
                        creator_user=change_username, revision_link=update.revision.link, is_subscriber=is_subscriber
                    )
            notifications.append(notification)
        return notifications
