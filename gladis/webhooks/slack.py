from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings


class SlackClient:
    client = WebClient(token=settings.SLACK_API_KEY)

    @staticmethod
    def add_to_slack_string(slack_string: str, addition: str, new_line=True):
        """add a string to a slack message string"""
        if new_line:
            return f"{slack_string}\n{addition}"
        return f"{slack_string}{addition}"

    def send_slack_message(self, message: str, slack_channel=None, slack_mention=None):
        """
        send slack message to a channel
        
        Args:
            message (str): message to send
            slack_channel (str): channel to send message to
            slack_mention (str): user to mention in message - username NOT email
        """
        if settings.SLACK_CHANNEL_OVERRIDE or not slack_channel:
            slack_channel = settings.SLACK_CHANNEL_OVERRIDE

        if settings.SLACK_MENTION_OVERRIDE or not slack_mention:
            slack_mention = settings.SLACK_MENTION_OVERRIDE

        try:
            response = self.client.chat_postMessage(
                channel=f"#{slack_channel}",
                text=f"<@{slack_mention}>\n---------------\n{message}",
            )
            print(response)
            return True
        except SlackApiError as e:
            print(f"ERROR: {e}")
            return False
