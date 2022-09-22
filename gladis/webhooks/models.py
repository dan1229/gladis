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
        # get pr information
        if self.payload.get("pull_request"):
            action = self.payload.get("action")
            if action and action == "opened":
                print("New PR opened!")
            elif action and action == "closed":
                print("PR closed!")
            print(f"\taction: {action}")
            # TODO handle draft statuses

            title = self.payload.get("pull_request", {}).get("title")
            if title:
                print(f"\ttitle: {title}")

            pr_number = self.payload.get("pull_request", {}).get("number")
            if pr_number:
                print(f"\tpr number: {pr_number}")

            state = self.payload.get("pull_request", {}).get("state")
            if state:
                print(f"\tstate: {state}")

            is_draft = self.payload.get("pull_request", {}).get("draft")
            is_draft = str_to_bool(is_draft)
            print(f"\tis draft: {is_draft}")

            github_user = (
                self.payload.get("pull_request", {}).get("user", {}).get("login")
            )
            github_user_link = (
                self.payload.get("pull_request", {}).get("user", {}).get("html_url")
            )
            if github_user:
                print(f"\tgithub user: {github_user}")
                print(f"\tgithub user link: {github_user_link}")

            repository = self.payload.get("repository", {}).get("full_name")
            repository_link = self.payload.get("repository", {}).get("html_url")
            if repository:
                print(f"\trepository: {repository}")
                print(f"\trepository link: {repository_link}")

            # TODO handle if switching base branch notification?

        # get workflow run information
        if self.payload.get("workflow_run"):
            action = self.payload.get("action")
            if action and action == "completed":
                print("\tWorkflow completed!")
            elif action and action == "requested":
                print("\tWorkflow requested!")

            workflow_name = self.payload.get("workflow", {}).get("name")
            workflow_state = self.payload.get("workflow_run", {}).get("state")
            workflow_url = self.payload.get("workflow", {}).get("html_url")
            print(f"\tworkflow name: {workflow_name}")
            print(f"\tworkflow state: {workflow_state}")
            print(f"\tworkflow url: {workflow_url}")

        # get workflow job information
        if self.payload.get("workflow_job"):
            action = self.payload.get("action")
            if action and action == "completed":
                print("\tWorkflow completed!")
            elif action and action == "requested":
                print("\tWorkflow requested!")

            workflow_name = self.payload.get("workflow_job", {}).get("name")
            workflow_status = self.payload.get("workflow_job", {}).get("status")
            workflow_url = self.payload.get("workflow_job", {}).get("html_url")
            print(f"\tworkflow name: {workflow_name}")
            print(f"\tworkflow status: {workflow_status}")
            print(f"\tworkflow url: {workflow_url}")
