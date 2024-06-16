class NotificationBuilder:
    def new_review_request(self, creator_user: str, revision_link: str) -> str:
        return f"{creator_user} has created a new revision and would like you to review it. Review here:{revision_link}"

    def new_update_review_request(self, creator_user: str, revision_link: str) -> str:
        return f"{creator_user} has added new changes to their revision. Review here:{revision_link}"

    def new_comment_by_owner(self, creator_user: str, revision_link: str) -> str:
        return f"{creator_user} has responded to a comment in their revision. Check it out: {revision_link}"

    def new_incoming_review(self, creator_user: str, revision_link: str) -> str:
        return f"{creator_user} has reviewed your changes. Check out their comments here:{revision_link}"

    def new_award(self, creator_user: str, revision_link: str, award: str) -> str:
        return f"{creator_user} gave you an award! Here you go, awesome job! {award} {revision_link}"

    def new_generic_update(self, creator_user: str, revision_link: str) -> str:
        return f"{creator_user} made an update on your revision. Check it out: {revision_link}"
