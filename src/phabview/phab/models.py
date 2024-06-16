import enum


class Reviewer:
    phid: str
    status: str

    def __init__(self, phid: str, status: str) -> None:
        self.phid = phid
        self.status = status

    @property
    def has_contributed(self) -> bool:
        return self.status != "added"


class Revision:
    phid: str
    owner: str
    reviewers: list[Reviewer]
    subscribers: list[str]
    link: str

    def __init__(self, raw_revision: dict):
        self.construct_from_raw(raw_revision)

    def construct_from_raw(self, raw_revision: dict):
        self.phid = raw_revision["phid"]
        self.link = raw_revision["fields"]["uri"]
        self.owner = raw_revision["fields"]["authorPHID"]
        self.subscribers = raw_revision["attachments"]["subscribers"].get(
            "subscriberPHIDs", [],
        )
        self.reviewers = []
        for reviewer in raw_revision["attachments"]["reviewers"]["reviewers"]:
            self.reviewers.append(
                Reviewer(phid=reviewer["reviewerPHID"], status=reviewer["status"]),
            )


class UpdateTypeEnum(enum.Enum):
    comment = "comment"
    create = "create"
    update = "update"
    generic = "generic"

    @classmethod
    def list(cls):
        return [c.value for c in cls]


class Update:
    update_type: str
    change_user: str
    revision: Revision

    def __init__(self, update_type: str, change_user: str, revision: Revision):
        self.update_type = update_type
        self.revision = revision
        self.change_user = change_user

    @property
    def to_be_notified_users(self) -> list[str]:
        match self.update_type:
            case UpdateTypeEnum.generic.value:
                notifiable_reviewers = []
            case UpdateTypeEnum.update.value | UpdateTypeEnum.create.value:
                notifiable_reviewers = [
                    reviewer.phid for reviewer in self.revision.reviewers
                ]
            case UpdateTypeEnum.comment.value:
                notifiable_reviewers = [
                    reviewer.phid
                    for reviewer in self.revision.reviewers
                    if reviewer.has_contributed
                ]
            case _:
                notifiable_reviewers = []

        users = set(
            [self.revision.owner] + self.revision.subscribers + notifiable_reviewers,
        )
        users.discard(self.change_user)
        return list(users)
