from dataclasses import dataclass

from slack import WebClient
from slackeventsapi import SlackEventAdapter  # type: ignore


@dataclass
class Bot:
    slack_event_adapter: SlackEventAdapter
    client: WebClient

    def __init__(self, slack_token, signing_secret, app):
        self.slack_event_adapter = SlackEventAdapter(
            signing_secret, "/slack/events", app
        )
        self.client = WebClient(token=slack_token)
