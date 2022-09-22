from django.db import models

from core.models import AbstractBaseModel
from core.helpers import str_to_bool
from webhooks.slack import Slack

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


class GithubWebhookReceiver(WebhookReceived):
    action = models.CharField(max_length=255, help_text="The action of the event.")
    
    pull_request = models.JSONField(default=None, null=True)
    workflow_run = models.JSONField(default=None, null=True)
    workflow_job = models.JSONField(default=None, null=True)
    
    def process_github_webhook(self, send_slack_message=True):
        slack_message = ''
        action = self.payload.get("action")
        self.action = action
        self.save()
        
        # get pr information
        if self.payload.get("pull_request"):
            # update object
            self.pull_request = self.payload.get("pull_request")
            slack_message = self.parse_pull_request()
            self.save()

        # get workflow run information
        if self.payload.get("workflow_run"):
            self.workflow_run = self.payload.get("workflow_run")
            slack_message = self.parse_workflow_run()
            self.save()

        # get workflow job information
        if self.payload.get("workflow_job"):
            self.workflow_job = self.payload.get("workflow_job")
            slack_message = self.parse_workflow_job()
            self.save()
            
        if send_slack_message:
            Slack.send_slack_message(slack_message)
        else:
            print(slack_message)


    def parse_pull_request(self):
        slack_message = ""
        
        action = self.payload.get("action")
        if action and action == "opened":
            slack_message = Slack.add_to_slack_string(slack_message, "\tPR opened! :tada:")
        elif action and action == "closed":
            slack_message = Slack.add_to_slack_string(slack_message, "\tPR closed! :tada:")
        Slack.add_to_slack_string(slack_message, "\taction: {action}")
        # TODO handle draft statuses

        title = self.payload.get("pull_request", {}).get("title")
        if title:
            slack_message = Slack.add_to_slack_string(slack_message, f"\ttitle: {title}")

        pr_number = self.payload.get("pull_request", {}).get("number")
        if pr_number:
            slack_message = Slack.add_to_slack_string(slack_message, f"\tpr number: {pr_number}")

        state = self.payload.get("pull_request", {}).get("state")
        if state:
            slack_message = Slack.add_to_slack_string(slack_message, f"\tstate: {state}")

        is_draft = self.payload.get("pull_request", {}).get("draft")
        is_draft = str_to_bool(is_draft)
        slack_message = Slack.add_to_slack_string(slack_message, f"\tdraft: {is_draft}")

        github_user = (
            self.payload.get("pull_request", {}).get("user", {}).get("login")
        )
        github_user_link = (
            self.payload.get("pull_request", {}).get("user", {}).get("html_url")
        )
        if github_user:
            slack_message = Slack.add_to_slack_string(slack_message, f"\tuser: {github_user}")
            slack_message = Slack.add_to_slack_string(slack_message, f"\tuser link: {github_user_link}")

        repository = self.payload.get("repository", {}).get("full_name")
        repository_link = self.payload.get("repository", {}).get("html_url")
        if repository:
            slack_message = Slack.add_to_slack_string(slack_message, f"\trepository: {repository}")
            slack_message = Slack.add_to_slack_string(slack_message, f"\trepository link: {repository_link}")

        merged = self.payload.get("pull_request", {}).get("merged")
        merged = str_to_bool(merged)
        slack_message = Slack.add_to_slack_string(slack_message, f"\tmerged: {merged}")

        # TODO
        # save reviewer and author info
        # handle if switching base branch notification?
        
        return slack_message
    
    
    def parse_workflow_run(self):
        slack_message = ''
        
        action = self.payload.get("action")
        slack_message = Slack.add_to_slack_string(slack_message, f"\tWorkflow {action}")
        if action and action == "completed":
            slack_message += ":tada:"
        elif action and action == "requested":
            slack_message += ":please:"
        elif action and action == "failed":
            slack_message += ":sad:"

        
        slack_message = Slack.add_to_slack_string(slack_message, f"\tid: {self.payload.get('workflow_run', {}).get('id')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\tname: {self.payload.get('workflow', {}).get('name')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\tstate: {self.payload.get('workflow_run', {}).get('state')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\turl: {self.payload.get('workflow', {}).get('html_url')}")
        
        return slack_message
    
    def parse_workflow_job(self):
        slack_message = ''
        
        action = self.payload.get("action")
        slack_message = Slack.add_to_slack_string(slack_message, f"\tWorkflow {action}")
        if action and action == "completed":
            slack_message += ":tada:"
        elif action and action == "requested":
            slack_message += ":please:"
        elif action and action == "failed":
            slack_message += ":sad:"
        
        slack_message = Slack.add_to_slack_string(slack_message, f"\id: {self.payload.get('workflow_job', {}).get('id')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\name: {self.payload.get('workflow_job', {}).get('name')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\state: {self.payload.get('workflow_job', {}).get('state')}")
        slack_message = Slack.add_to_slack_string(slack_message, f"\url: {self.payload.get('workflow_job', {}).get('html_url')}")
        
        return slack_message