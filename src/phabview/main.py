from http import HTTPStatus
from asgiref.wsgi import WsgiToAsgi
from phabview.config import PHABRICATOR_HMAC_HEADER_NAME
from flask import Flask, Response, request
from phabview.phabview import PhabView

app = Flask("PhabView")


@app.route("/receive_webhook", methods=["POST"])
async def receive_webhook():
    phabview = PhabView()
    hmac_header = request.headers.get(PHABRICATOR_HMAC_HEADER_NAME)
    phabview.verify_hmac(request_data=request.data, hmac_header=hmac_header)
    await phabview.handle(request.json)

    return Response(status=HTTPStatus.OK)


asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)
