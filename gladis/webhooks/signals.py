# from webhooks.slack import SlackClient
from django.db.models.signals import post_save
from django.dispatch import receiver

from webhooks.models.github import GithubPullRequest, GithubWorkflow
from webhooks.slack import SlackClient


@receiver(post_save, sender=GithubPullRequest)
def github_pull_request_handle_messages(sender, instance, created, **kwargs):
    send_message_pr_opened(instance)
    send_message_pr_merged(instance)
    send_message_pr_closed(instance)


@receiver(post_save, sender=GithubWorkflow)
def github_workflow_handle_messages(sender, instance, created, **kwargs):
    send_message_ci_passing(instance)
    send_message_ci_failing(instance)


#
# SLACK MESSAGING FUNCTIONS
#
def send_message_ci_passing(workflow):
    # TODO should message only be sent if PR is not in draft?
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
        if slack_author_username:
            SlackClient().send_slack_direct_message(
                slack_message, slack_author_username
            )

        try:
            pull_request = GithubPullRequest.objects.get(
                github_id=workflow.pull_request_github_id
            )
            for reviewer in pull_request.reviewers:
                slack_reviewer_username = (
                    SlackClient.get_slack_username_from_github_username(reviewer)
                )
                if slack_reviewer_username:
                    SlackClient().send_slack_direct_message(
                        slack_message, slack_reviewer_username
                    )
        except GithubPullRequest.DoesNotExist:
            print(
                f"ERROR: send_message_ci_passing: no pull request found. Workflow ID: {workflow.id}"
            )


def send_message_ci_failing(workflow):
    # TODO should message only be sent if PR is not in draft?
    if workflow.status == "completed" and workflow.conclusion == "failure":
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "CI failed! You suck! :feelsbadman:"
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
        if slack_author_username:
            SlackClient().send_slack_direct_message(
                slack_message, slack_author_username
            )


def send_message_pr_opened(pull_request):
    if pull_request.action == "opened":
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "PR opened! :open_hands:"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"author: {pull_request.github_user}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request id: {pull_request.github_id}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request link: {pull_request.pull_request_url}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"repository link: {pull_request.repository_link}"
        )

        slack_author_username = SlackClient.get_slack_username(pull_request.github_user)
        if slack_author_username:
            SlackClient().send_slack_direct_message(
                slack_message, slack_author_username
            )


def send_message_pr_merged(pull_request):
    if pull_request.is_merged:
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "PR merged! :tada:"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"author: {pull_request.github_user}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request id: {pull_request.github_id}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request link: {pull_request.pull_request_url}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"repository link: {pull_request.repository_link}"
        )

        slack_author_username = SlackClient.get_slack_username(pull_request.github_user)
        if slack_author_username:
            SlackClient().send_slack_direct_message(
                slack_message, slack_author_username
            )

        for reviewer in pull_request.reviewers:
            slack_reviewer_username = (
                SlackClient.get_slack_username_from_github_username(reviewer)
            )
            if slack_reviewer_username:
                send_message_pr_ready_for_review(pull_request, reviewer)


def send_message_pr_ready_for_review(pull_request, slack_reviewer_username):
    if not pull_request.is_draft:
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "PR ready for review! :eyes:"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "-------------------"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"author: {pull_request.github_user}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request id: {pull_request.github_id}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"pull request link: {pull_request.pull_request_url}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"repository link: {pull_request.repository_link}"
        )

        SlackClient().send_slack_direct_message(slack_message, slack_reviewer_username)


def send_message_pr_closed(pull_request):
    # TODO do we want this?
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
