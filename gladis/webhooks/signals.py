# from webhooks.slack import SlackClient
from django.db.models.signals import post_save
from django.dispatch import receiver

from webhooks.models.github import GithubPullRequest, GithubWorkflow


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
    # TODO - distinguish between 'workflow_run' and 'workflow_job' events
    # TODO send messages

    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"Workflow {action}"
    # )
    # slack_message = add_workflow_status_emoji(slack_message, payload)
    # slack_message = SlackClient.add_to_slack_string(
    #     slack_message, f"id: {github_id}"
    # )
    # slack_message = SlackClient.add_to_slack_string(slack_message, f"name: {name}")
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