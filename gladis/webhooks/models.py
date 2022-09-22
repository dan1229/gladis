from django.db import models

from core.models import AbstractBaseModel
from core.helpers import str_to_bool


#
# WEBHOOK RECEIVED ====================================== #
#
class WebhookReceived(AbstractBaseModel):
    received_at = models.DateTimeField(help_text="When we received the event.")
    sender = models.CharField(max_length=255, help_text="The sender of the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return f"Webhook ({self.id}): {self.received_at}"

    @property
    def get_property_action(self):
        return self.payload.get("action")
    
    def process_github_webhook(self):
        action = self.payload.get("action")
        if action and action == 'opened':
            print("New PR opened!")
        elif action and action == 'closed':
            print("PR closed!")
            
        title = self.payload.get("pull_request", {}).get("title")
        if title:
            print(f"\ttitle: {title}")
            
        pr_number =  self.payload.get("pull_request", {}).get("number")
        if pr_number:
            print(f"\tpr number: {pr_number}")
        
        state = self.payload.get("pull_request", {}).get("state")
        if state:
            print(f"\tstate: {state}")
            
        is_draft = self.payload.get("pull_request", {}).get("draft")
        is_draft = str_to_bool(is_draft)
        print(f"\tis draft: {is_draft}")
            
        github_user = self.payload.get("pull_request", {}).get("user", {}).get("login")
        github_user_link = self.payload.get("pull_request", {}).get("user", {}).get("html_url")
        if github_user:
            print(f"\tgithub user: {github_user}")
            print(f"\tgithub user link: {github_user_link}")
            
        repository = self.payload.get("repository", {}).get("full_name")
        repository_link = self.payload.get("repository", {}).get("html_url")
        if repository:
            print(f"\trepository: {repository}")
            print(f"\trepository link: {repository_link}")
            
    