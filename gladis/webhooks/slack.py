from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings
from core.models import UserSettings


class SlackClient:
    client = WebClient(token=settings.SLACK_API_KEY)

    @staticmethod
    def get_slack_username(github_username):
        """Get slack username from github username"""
        user_settings_queryset = UserSettings.objects.filter(github_username=github_username)
        if user_settings_queryset.count() == 0:
            return None
        return user_settings_queryset.first().slack_username

    @staticmethod
    def add_to_slack_string(slack_string: str, addition: str, new_line=True):
        """add a string to a slack message string"""
        if slack_string == "":
            return f"{addition}\n"
        if new_line:
            return f"{slack_string}\n{addition}"
        return f"{slack_string}{addition}"

    #
    # SEND MESSAGES
    #
    def send_slack_direct_message(self, message: str, slack_username: str):
        """
        send slack message to a channel

        Args:
            message (str): message to send
            slack_username (str): user to send message to - username NOT email
        """
        try:

            self.client.chat_postMessage(
                channel="#botdev",
                text=f"<@{slack_username}>\n---------------\n{message}",
            )
            # TODO switch to dms once bot gets permissions
            # conversations = self.client.conversations_open(users=[slack_username])
            # conversations.send_message(channel=conversations.channel.id, text=message)
            return True
        except SlackApiError as e:
            print(f"ERROR (send_slack_direct_message): {e}")
            return False

    def send_slack_message_to_channel(
        self, message: str, slack_channel=None, slack_mention=None
    ):
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
            self.client.chat_postMessage(
                channel=f"#{slack_channel}",
                text=f"<@{slack_mention}>\n---------------\n{message}",
            )
            return True
        except SlackApiError as e:
            print(f"ERROR (send_slack_message_to_channel): {e}")
            return False
