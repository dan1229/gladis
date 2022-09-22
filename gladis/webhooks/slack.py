import os
from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings

client = WebClient(token=settings.SLACK_API_KEY)

def send_slack_message(message, slack_channel=None, slack_mention=None):
    if settings.SLACK_CHANNEL_OVERRIDE or not slack_channel:
        slack_channel = settings.SLACK_CHANNEL_OVERRIDE
        
    if settings.SLACK_MENTION_OVERRIDE or not slack_mention:
        slack_mention = settings.SLACK_MENTION_OVERRIDE
        
    try:
        response = client.chat_postMessage(
            channel=f"#{slack_channel}",
            text=f"@{slack_mention} - {message}")
        print(response)
    except SlackApiError as e:
        print(f"ERROR: {e}")