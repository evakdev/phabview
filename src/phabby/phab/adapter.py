from phabby.config import PHABRICATOR_HOST, PHABRICATOR_TOKEN, PHABRICATOR_USERNAME
from phabricator import Phabricator


class PhabricatorAdapter:
    def __init__(self):
        self.api = Phabricator(
            host=PHABRICATOR_HOST,
            username=PHABRICATOR_USERNAME,
            token=PHABRICATOR_TOKEN,
        )
        self.api.update_interfaces()

    def get_revision(
        self,
        phid: str,
    ) -> dict | None:
        revisions = self.api.differential.revision.search(
            constraints={"phids": [phid]},
            attachments={"reviewers": True, "subscribers": True},
        ).get("data", [])
        if revisions:
            return revisions[0]
        return None

    def get_transactions(self, object_phid: str, transaction_phids: list[str]) -> list:
        return self.api.transaction.search(
            objectIdentifier=object_phid,
            constraints={"phids": transaction_phids},
        ).get("data", [])

    def get_user(self, phid: str) -> dict | None:
        users = self.api.user.search(constraints={"phids": [phid]}).get("data", [])
        if users:
            return users[0]
        return None

    def get_user_username(self, phid: str) -> str | None:
        user_object = self.get_user(phid)
        if user_object:
            return user_object["fields"]["username"]
        return None
