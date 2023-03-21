from flask import Flask

from slacker.backend.bot import Bot
from slacker.backend.commands import bot_command
from slacker.backend.response import Response, make_response
from slacker.handle_request import RequestHandler

app = Flask(__name__)

__all__ = ["run", "make_response", "Response", "bot_command"]


def run(slack_token, signing_secret, debug=True):
    bot = Bot(slack_token, signing_secret, app)
    handler = RequestHandler(bot)
    handler.start()
    app.run(debug=debug)
