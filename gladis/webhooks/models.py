from django.db import models

from core.models import AbstractBaseModel
from webhooks.slack import SlackClient
from webhooks.github_parser import GithubParser


#
# WEBHOOK RECEIVED ====================================== #
#
class WebhookReceived(AbstractBaseModel):
    received_at = models.DateTimeField(help_text="When we received the event.")
    sender = models.CharField(max_length=255, help_text="The sender of the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        ordering = ["-received_at"]
        indexes = [
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return f"Webhook ({self.id}): {self.received_at}"

    @property
    def get_property_action(self):
        return self.payload.get("action")


#
# GITHUB WEBHOOK RECEIVED ====================================== #
#
class GithubWebhookReceived(WebhookReceived):
    action = models.CharField(max_length=255, help_text="The action of the event.")
    webhook_type = models.CharField(max_length=255, help_text="The type of webhook.")

    pull_request = models.JSONField(default=None, null=True)
    workflow_run = models.JSONField(default=None, null=True)
    workflow_job = models.JSONField(default=None, null=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self):
        return (
            f"Github Webhook ({self.webhook_type} - {self.action}): {self.received_at}"
        )

    #
    # FUNCTIONS ====================================== #
    #
    def user_is_involved(self):
        """Check if the user is involved in the event."""
        user = self.payload.get("actor", {}).get("login")
        if not user:
            user = self.payload.get("triggering_actor", {}).get("login")
        if not user:  # this is present on workflow_run/job and pull_request
            user = self.payload.get("sender", {}).get("login")
        if not user:
            user = self.payload.get("pull_request", {}).get("user", {}).get("login")
        return SlackClient.get_slack_username(user) is not None

    def process_github_webhook(self, send_slack_message=True):
        action = self.payload.get("action")
        self.action = action
        self.save()

        # get pr information
        if self.payload.get("pull_request"):
            self.pull_request = self.payload.get("pull_request")
            self.webhook_type = "pull_request"
            GithubParser().parse_pull_request(self.payload, send_slack_message)
            self.save()

        # get workflow run information
        if self.payload.get("workflow_run"):
            self.workflow_run = self.payload.get("workflow_run")
            self.webhook_type = "workflow_run"
            GithubParser().parse_workflow_run(self.payload, send_slack_message)
            self.save()

        # get workflow job information
        if self.payload.get("workflow_job"):
            self.workflow_job = self.payload.get("workflow_job")
            self.webhook_type = "workflow_job"
            GithubParser().parse_workflow_job(self.payload, send_slack_message)
            self.save()
