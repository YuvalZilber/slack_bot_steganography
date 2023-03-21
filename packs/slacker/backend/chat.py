import slack

from packs.slacker.backend.commands import allowed_commands


class Chat:
    def __init__(self, web_client: slack.WebClient, channel_id: str, prefix: str = ""):
        self._web_client = web_client
        self._channel_id = channel_id
        self._prefix = prefix and f"[{prefix}] "
        self._has_error = False

    def post_message(self, text="", *, prefix="", **kwargs) -> None:
        prefix = f"{prefix}{self._prefix}"
        kwargs["text"] = f"{prefix}{text}".strip()
        self._web_client.chat_postMessage(channel=self._channel_id, **kwargs)

    def post_error(self, text="", **kwargs) -> None:
        self._has_error = True
        self.post_message(text=text, prefix=f"[ERROR] ", **kwargs)

    # def post_response(self, response: Response) -> None:
    #     warn('post_response', DeprecationWarning, stacklevel=2)
    #     text = hasattr(response, "text") and hasattr(response.text, "_value") and response.text._value
    #     if hasattr(response, "image") and hasattr(response.image, "_value") and response.image._value:
    #         file = os.path.abspath(response.image._value)
    #         self._web_client.files_upload(
    #             file=file,
    #             initial_comment=text or "",
    #             channels=self._channel_id
    #         )
    #     elif text:
    #         self.post_message(text=response.text._value)
    #     else:
    #         raise ValueError("response has to have either 'text' or 'image' attribute with a truthy value")

    @property
    def has_error(
        self,
    ) -> (
        bool
    ):  # note: i usually not support this "public property" but it is the only attr to expose
        return self._has_error

    def extract_command(self, event) -> str:
        text: str = event.get("text")
        if not text.startswith("\\"):
            self.post_error(f"commands to this bot must start with \\")
            return ""
        parts = text.split(" ")
        cmd = parts[0].strip("\\")
        if cmd not in allowed_commands():
            self.post_error(
                f"command '{cmd}' not found, try command \\help for more information"
            )
            if "help" in allowed_commands():
                allowed_commands()["help"](**event)
        event["text"] = " ".join(parts[1:])
        return cmd
