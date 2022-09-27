# from webhooks.slack import SlackClient
from django.db.models.signals import post_save
from django.dispatch import receiver

from webhooks.models.github import GithubPullRequest, GithubWorkflow
from webhooks.slack import SlackClient


@receiver(post_save, sender=GithubPullRequest)
def github_pull_request_handle_messages(sender, instance, created, **kwargs):
    pass


@receiver(post_save, sender=GithubWorkflow)
def github_workflow_handle_messages(sender, instance, created, **kwargs):
    send_message_ci_passing(instance)
    send_message_ci_failing(instance)


#
# SLACK MESSAGING FUNCTIONS
#
def send_message_ci_passing(workflow):
    if workflow.status == "completed" and workflow.conclusion == "success":
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "CI passing! :tada:"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow name: {workflow.name}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"author: {workflow.github_user}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"repository link: {workflow.repository_link}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow link: {workflow.workflow_url}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow id: {workflow.github_id}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow status: {workflow.status}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow conclusion: {workflow.conclusion}"
        )

        slack_author_username = SlackClient.get_slack_username(workflow.github_user)
        SlackClient().send_slack_direct_message(slack_message, slack_author_username)

        try:
            pull_request = GithubPullRequest.objects.get(
                github_id=workflow.pull_request_github_id
            )
            for reviewer in pull_request.requested_reviewers:
                slack_reviewer_username = (
                    SlackClient.get_slack_username_from_github_username(reviewer)
                )
                SlackClient().send_slack_direct_message(
                    slack_message, slack_reviewer_username
                )
        except GithubPullRequest.DoesNotExist:
            print(
                f"ERROR: send_message_ci_passing: no pull request found. Workflow ID: {workflow.id}"
            )

def send_message_ci_failing(workflow):
    if workflow.status == "completed" and workflow.conclusion == "failure":
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(slack_message, "CI failed! You suck! :feelsbadman:")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow name: {workflow.name}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"author: {workflow.github_user}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"repository link: {workflow.repository_link}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow link: {workflow.workflow_url}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow id: {workflow.github_id}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow status: {workflow.status}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"workflow conclusion: {workflow.conclusion}"
        )

        slack_author_username = SlackClient.get_slack_username(workflow.github_user)
        SlackClient().send_slack_direct_message(slack_message, slack_author_username)





# TODO
# - pr opened
#   - send to author
def send_message_pr_opened(instance):
    pass


# TODO
# - pr merged
#   - send to author
#   - send to reviewers
def send_message_pr_merged(instance):
    pass


# TODO
# - pr closed
def send_message_pr_closed(instance):
    pass


def add_workflow_status_emoji(slack_message, payload):
    action = payload.get("action")
    if action and action == "completed":
        slack_message += ":tada:"
    elif action and action == "requested":
        slack_message += ":please:"
    elif action and action == "failed":
        slack_message += ":sad:"
    elif action and action == "queued":
        slack_message += ":sonic-waiting:"
    return slack_message
