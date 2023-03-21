import traceback
from pprint import pprint

from packs.slacker.backend.bot import Bot
from packs.slacker.backend.chat import Chat
from packs.slacker.backend.commands import allowed_commands
from packs.slacker.backend.response import to_message


class RequestHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    def start(self):
        self.bot.slack_event_adapter.add_listener("message", self.handle_request)

    def handle_request(self, payload: dict) -> None:
        try:
            self._handle_payload(payload)
        except Exception as e:
            self.bot.client.chat_postMessage(
                channel=payload["event"]["channel"], text="Fatal Error"
            )
            print(self._get_traceback(e))

    def _handle_payload(self, payload: dict) -> None:
        event = payload.get("event", {})
        if event.get("bot_id"):  # I get my own messages
            return
        pprint(payload)

        chat = Chat(self.bot.client, event["channel"], event.get("user"))
        cmd = chat.extract_command(event)

        if chat.has_error:
            return
        try:
            response = allowed_commands()[cmd](**event)
            # chat.post_response(response)
            chat.post_message(blocks=to_message(response))
        except Exception as e:
            chat.post_error("Unknown Error")
            print(self._get_traceback(e))

    @staticmethod
    def _get_traceback(e):
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        return "".join(lines)
