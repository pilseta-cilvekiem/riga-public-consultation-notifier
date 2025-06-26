from urllib import parse

from slack_sdk import WebClient

from ..models.public_consultation import PublicConsultation
from ..parameters import ROOT_URL, SLACK_CHANNEL_ID, get_slack_bot_user_oauth_token


class SlackNotifier:
    def __init__(self) -> None:
        self.slack_client = WebClient(token=get_slack_bot_user_oauth_token())

    def post_message(self, message: str) -> None:
        self.slack_client.chat_postMessage(  # type: ignore
            channel=SLACK_CHANNEL_ID,
            text=message,
        )

    def post_public_consultation(self, public_consultation: PublicConsultation) -> None:
        message_lines = [
            public_consultation.type.display_name,
            f"*<{ROOT_URL}{parse.quote(public_consultation.path)}|{_escape(public_consultation.description)}>*",
        ]
        for field_label, field_value in public_consultation.fields.items():
            message_lines.append(f"{_escape(field_label)}: {_escape(field_value)}")
        message = "\n".join(message_lines)
        self.post_message(message)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
