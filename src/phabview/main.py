import hashlib
import hmac
from http import HTTPStatus
from asgiref.wsgi import WsgiToAsgi
from phabview.config import (
    NOTIFIABLE_USERS,
    NOTIFY_ANY_USER,
    PHABRICATOR_HMAC_HEADER_NAME,
    PHABRICATOR_REVISION_TYPE_NAME,
    PHABRICATOR_WEBHOOK_HMAC_KEY,
)
from flask import Flask, Response, request

from phabview.adapters.adapter_factory import AdapterFactory
from phabview.phab.update_manager import UpdateManager

app = Flask("PhabView")


@app.route("/receive_webhook", methods=["POST"])
async def receive_webhook():
    # hmac_object = hmac.new(
    #     key=bytes(PHABRICATOR_WEBHOOK_HMAC_KEY, "utf-8"),
    #     msg=request.data,
    #     digestmod=hashlib.sha256,
    # )
    # signature = hmac_object.hexdigest()
    # hmac_header = request.headers.get(PHABRICATOR_HMAC_HEADER_NAME)
    # if hmac_header != signature:
    #     raise Exception
    data = request.json
    changed_object = data["object"]

    if changed_object["type"] != PHABRICATOR_REVISION_TYPE_NAME:
        return Response(status=HTTPStatus.OK)

    transactions = []
    for transaction in data["transactions"]:
        transactions.extend(transaction.values())

    phabricator_update_manager = UpdateManager()
    update = phabricator_update_manager.get_update(changed_object, transactions)
    if not update:
        return Response(status=HTTPStatus.OK)
    notifications = phabricator_update_manager.create_notifs(update)
    messaging_adapter = AdapterFactory().get_adapter()
    if NOTIFY_ANY_USER:
        for notification in notifications:
            print(f'to {notification["user"]}: {notification["text"]}')
            # await messaging_adapter.send(notification["user"], notification["text"])
        return Response(status=HTTPStatus.OK)
    for notification in notifications:
        if notification["user"] in NOTIFIABLE_USERS:
            await messaging_adapter.send(notification["user"], notification["text"])
    return Response(status=HTTPStatus.OK)


asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)