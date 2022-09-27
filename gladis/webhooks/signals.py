# from webhooks.slack import SlackClient
from django.db.models.signals import post_save
from django.dispatch import receiver

from webhooks.models.github import GithubPullRequest, GithubWorkflow
from webhooks.slack import SlackClient


@receiver(post_save, sender=GithubPullRequest)
def github_pull_request_handle_messages(sender, instance, created, **kwargs):
    pass
    # TODO send messages
    # if action and action == "opened":
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, "PR opened! :tada:"
    #     )
    # elif action and action == "closed":
    #     if merged:
    #         self.send_slack_message_to_user(
    #             "Congrats! Your PR was merged! :tada:",
    #             payload.get("pull_request", {}).get("user", {}).get("login"),
    #         )
    #         slack_message = SlackClient.add_to_slack_string(
    #             slack_message, "PR merged! :merged_parrot:"
    #         )
    #     else:
    #         slack_message = SlackClient.add_to_slack_string(
    #             slack_message, "PR closed! :sad:"
    #         )
    # SlackClient.add_to_slack_string(slack_message, "action: {action}")
    # if title:
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"title: {title}"
    #     )

    # if pr_number:
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"pr number: {pr_number}"
    #     )

    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"id: {github_id}"
    # )
    # if state:
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"state: {state}"
    #     )
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"draft: {is_draft}"
    # )

    # if github_user:
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"user: {github_user}"
    #     )
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"user link: {github_user_link}"
    #     )
    # if repository:
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"repository: {repository}"
    #     )
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"repository link: {repository_link}"
    #     )
    # if requested_reviewers and len(requested_reviewers > 0):
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"requested reviewers: {requested_reviewers}"
    #     )


@receiver(post_save, sender=GithubWorkflow)
def github_workflow_handle_messages(sender, instance, created, **kwargs):
    pass
    # TODO send messages
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"Workflow {action}"
    # )
    # slack_message = add_workflow_status_emoji(slack_message, payload)
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"id: {github_id}"
    # )
    # slack_message = SlackClient.add_to_slack_string(slack_message, f"name: {name}")
    # TODO - distinguish between 'workflow_run' and 'workflow_job' events via payload
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, "webhook type: workflow run"
    # )
    # if status and status != "":
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message,
    #         f"status: {status}",
    #     )
    # if conclusion and conclusion != "":
    #     slack_message = SlackClient.add_to_slack_string(
    #         slack_message, f"conclusion: {conclusion}"
    #     )
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"url: {"
    # )


#
# MESSAGING FUNCTIONS
#


# TODO
# - ci passing
#   - send to author
#   - send to reviewers
def send_message_ci_passing(workflow):
    if workflow.status == "completed" and workflow.conclusion == "success":
        slack_message = ""
        slack_message = SlackClient.add_to_slack_string(slack_message, "CI passing! :tada:")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"-------------------")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"workflow name: {workflow.name}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"author: {workflow.github_user}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"-------------------")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"repository: {workflow.repository}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"repository link: {workflow.repository_link}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"workflow link: {workflow.url}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"workflow id: {workflow.github_id}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"workflow status: {workflow.status}")
        slack_message = SlackClient.add_to_slack_string(slack_message, f"workflow conclusion: {workflow.conclusion}")
        
        slack_author_username = SlackClient.get_slack_username_from_github_username(workflow.github_user)
        SlackClient().send_slack_direct_message(slack_message, slack_author_username)
        
        for reviewer in workflow.requested_reviewers:
            slack_reviewer_username = SlackClient.get_slack_username_from_github_username(reviewer)
            SlackClient().send_slack_direct_message(slack_message, slack_reviewer_username)
        


# TODO
# - ci failing
#   - send to author
def send_message_ci_failing(instance):
    pass


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
