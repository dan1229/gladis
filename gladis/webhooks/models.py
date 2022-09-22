from django.db import models

from core.models import AbstractBaseModel
from core.helpers import str_to_bool
from webhooks.slack import SlackClient


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
        return f"Github Webhook ({self.webhook_type} - {self.action}): {self.received_at}"

    def process_github_webhook(self, send_slack_message=True):
        slack_message = ""
        action = self.payload.get("action")
        self.action = action
        self.save()

        # get pr information
        if self.payload.get("pull_request"):
            self.pull_request = self.payload.get("pull_request")
            self.webhook_type = "pull_request"
            slack_message = self.parse_pull_request()
            self.save()

        # get workflow run information
        if self.payload.get("workflow_run"):
            self.workflow_run = self.payload.get("workflow_run")
            self.webhook_type = "workflow_run"
            slack_message = self.parse_workflow_run()
            self.save()

        # get workflow job information
        if self.payload.get("workflow_job"):
            self.workflow_job = self.payload.get("workflow_job")
            self.webhook_type = "workflow_job"
            slack_message = self.parse_workflow_job()
            self.save()

        if send_slack_message:
            SlackClient().send_slack_message(slack_message)
        else:
            print(slack_message)

    def parse_pull_request(self):
        slack_message = ""

        action = self.payload.get("action")
        if action and action == "opened":
            slack_message = SlackClient.add_to_slack_string(
                slack_message, "PR opened! :tada:"
            )
        elif action and action == "closed":
            slack_message = SlackClient.add_to_slack_string(
                slack_message, "PR closed! :tada:"
            )
        SlackClient.add_to_slack_string(slack_message, "action: {action}")
        # TODO handle draft statuses

        title = self.payload.get("pull_request", {}).get("title")
        if title:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"title: {title}"
            )

        pr_number = self.payload.get("pull_request", {}).get("number")
        if pr_number:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"pr number: {pr_number}"
            )

        state = self.payload.get("pull_request", {}).get("state")
        if state:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"state: {state}"
            )

        is_draft = self.payload.get("pull_request", {}).get("draft")
        is_draft = str_to_bool(is_draft)
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"draft: {is_draft}"
        )

        github_user = self.payload.get("pull_request", {}).get("user", {}).get("login")
        github_user_link = (
            self.payload.get("pull_request", {}).get("user", {}).get("html_url")
        )
        if github_user:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"user: {github_user}"
            )
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"user link: {github_user_link}"
            )

        repository = self.payload.get("repository", {}).get("full_name")
        repository_link = self.payload.get("repository", {}).get("html_url")
        if repository:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"repository: {repository}"
            )
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"repository link: {repository_link}"
            )

        merged = self.payload.get("pull_request", {}).get("merged")
        merged = str_to_bool(merged)
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"merged: {merged}"
        )

        # TODO
        # save reviewer and author info
        # handle if switching base branch notification?

        return slack_message

    def parse_workflow_run(self):
        slack_message = ""

        action = self.payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        if action and action == "completed":
            slack_message += ":tada:"
        elif action and action == "requested":
            slack_message += ":please:"
        elif action and action == "failed":
            slack_message += ":sad:"

        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {self.payload.get('workflow_run', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {self.payload.get('workflow', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"state: {self.payload.get('workflow_run', {}).get('state')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"url: {self.payload.get('workflow', {}).get('html_url')}"
        )

        return slack_message

    def parse_workflow_job(self):
        slack_message = ""

        action = self.payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        if action and action == "completed":
            slack_message += ":tada:"
        elif action and action == "requested":
            slack_message += ":please:"
        elif action and action == "failed":
            slack_message += ":sad:"

        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {self.payload.get('workflow_job', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"ame: {self.payload.get('workflow_job', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"state: {self.payload.get('workflow_job', {}).get('state')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"url: {self.payload.get('workflow_job', {}).get('html_url')}",
        )

        return slack_message
