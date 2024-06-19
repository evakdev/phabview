class NotificationBuilder:
    def new_review_request(self, creator_user: str, revision_link: str, is_subscriber=False) -> str:
        if is_subscriber:
            return (
                f"{creator_user} has created a new review and you "
                f"have been subscribed. Check it out here: {revision_link}"
            )
        return (
            f"{creator_user} has created a new revision and would like you to review it. Review here: {revision_link}"
        )

    def new_update_review_request(self, creator_user: str, revision_link: str, is_subscriber=False) -> str:
        if is_subscriber:
            return (
                f"{creator_user} has added new changes to a revision "
                f"you're subscribed to. Check it out here: {revision_link}"
            )
        return f"{creator_user} has added new changes to their revision. Review here: {revision_link}"

    def new_comment_by_owner(self, creator_user: str, revision_link: str, is_subscriber=False) -> str:
        if is_subscriber:
            return (
                f"{creator_user} has responded to a comment in a revision "
                f"you're subscribed to. Check it out: {revision_link}"
            )
        return f"{creator_user} has responded to a comment in their revision. Check it out: {revision_link}"

    def new_incoming_review_generic(
        self, creator_user: str, revision_link: str, is_subscriber=False
    ) -> str:
        if is_subscriber:
            return (
                f"{creator_user} has reviewed changes in a revision you're subscribed to. "
                f"Check it out here: {revision_link}"
            )
        return f"{creator_user} has reviewed changed in one of your assigned reviews. Add yours here: {revision_link}"

    def new_incoming_review_for_owner(self, creator_user: str, revision_link: str):
        return f"{creator_user} has reviewed your changes. Check out their comments here: {revision_link}"

    def new_generic_update(self, creator_user: str, revision_link: str, is_subscriber=False) -> str:
        if is_subscriber:
            return (
                f"{creator_user} made an update to a revision you're subscribed to. "
                f"Check it out here: {revision_link}"
            )
        return f"{creator_user} made an update on your revision. Check it out: {revision_link}"
