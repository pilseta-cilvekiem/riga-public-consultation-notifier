from urllib import parse

from slack_sdk import WebClient

from ..constants import ROOT_URL
from ..models.public_consultation import PublicConsultation
from ..utils import get_required_environment_variable, get_secret_value


class SlackNotifier:
    def __init__(self) -> None:
        self.slack_client = WebClient(
            token=get_secret_value("slack_bot_user_oauth_token")
        )
        self.slack_channel_id = get_required_environment_variable("SLACK_CHANNEL_ID")

    def post_message(self, message: str) -> None:
        self.slack_client.chat_postMessage(
            channel=self.slack_channel_id,
            text=message,
        )

    def post_public_consultation(self, public_consultation: PublicConsultation) -> None:
        if public_consultation.is_closed:
            return

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
