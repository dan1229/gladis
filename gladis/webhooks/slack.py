import os
from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings

client = WebClient(token=settings.SLACK_API_KEY)

def send_slack_message(message):
    try:
        response = client.chat_postMessage(
            channel='#' + settings.SLACK_CHANNEL_OVERRIDE,
            text=message)
        print(response)
    except SlackApiError as e:
        print(f"ERROR: {e}")