from django.db import models

from core.models import AbstractBaseModel
from core.helpers import str_to_bool
from webhooks.slack import send_slack_message


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

    def process_github_webhook(self, should_send_slack_message=True):
        slack_message = ''
        # get pr information
        if self.payload.get("pull_request"):
            action = self.payload.get("action")
            if action and action == "opened":
                slack_message += "New PR opened! :tada:\n"
            elif action and action == "closed":
                slack_message += "PR closed!"
            slack_message += f"\taction: {action}\n"
            # TODO handle draft statuses

            title = self.payload.get("pull_request", {}).get("title")
            if title:
                slack_message += f"\ttitle: {title}\n"

            pr_number = self.payload.get("pull_request", {}).get("number")
            if pr_number:
                slack_message += f"\tpr number: {pr_number}\n"

            state = self.payload.get("pull_request", {}).get("state")
            if state:
                slack_message += f"\tstate: {state}\n"

            is_draft = self.payload.get("pull_request", {}).get("draft")
            is_draft = str_to_bool(is_draft)
            slack_message += f"\tis draft: {is_draft}\n"

            github_user = (
                self.payload.get("pull_request", {}).get("user", {}).get("login")
            )
            github_user_link = (
                self.payload.get("pull_request", {}).get("user", {}).get("html_url")
            )
            if github_user:
                slack_message += f"\tgithub user: {github_user}\n"
                slack_message += f"\tgithub user link: {github_user_link}\n"

            repository = self.payload.get("repository", {}).get("full_name")
            repository_link = self.payload.get("repository", {}).get("html_url")
            if repository:
                slack_message += f"\trepository: {repository}\n"
                slack_message += f"\trepository link: {repository_link}\n"

            merged = self.payload.get("pull_request", {}).get("merged")
            merged = str_to_bool(merged)
            slack_message += f"\tmerged: {merged}\n"

            # TODO handle if switching base branch notification?
            

        # get workflow run information
        if self.payload.get("workflow_run"):
            action = self.payload.get("action")
            if action and action == "completed":
                slack_message += "\tWorkflow completed! :tada:\n"
            elif action and action == "requested":
                slack_message += "\tWorkflow requested! :tada:\n"

            workflow_name = self.payload.get("workflow", {}).get("name")
            workflow_state = self.payload.get("workflow_run", {}).get("state")
            workflow_url = self.payload.get("workflow", {}).get("html_url")
            slack_message += f"\tworkflow name: {workflow_name}\n"
            slack_message += f"\tworkflow state: {workflow_state}\n"
            slack_message += f"\tworkflow url: {workflow_url}\n"

        # get workflow job information
        if self.payload.get("workflow_job"):
            action = self.payload.get("action")
            if action and action == "completed":
                slack_message += "\tWorkflow completed! :tada:\n"
            elif action and action == "requested":
                slack_message += "\tWorkflow requested! :tada:\n"

            workflow_name = self.payload.get("workflow_job", {}).get("name")
            workflow_status = self.payload.get("workflow_job", {}).get("status")
            workflow_url = self.payload.get("workflow_job", {}).get("html_url")
            slack_message += f"\tworkflow name: {workflow_name}\n"
            slack_message += f"\tworkflow status: {workflow_status}\n"
            slack_message += f"\tworkflow url: {workflow_url}\n"
            
        if should_send_slack_message:
            send_slack_message(slack_message)
