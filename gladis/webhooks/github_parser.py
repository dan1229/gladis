from webhooks.slack import SlackClient
from webhooks.models import GithubPullRequest, GithubWorkflow

from core.helpers import str_to_bool


class GithubParser:
    def send_slack_message_to_user(
        self, message, github_username, send_slack_message=True
    ):
        if send_slack_message:
            slack_username = SlackClient.get_slack_username(github_username)
            if slack_username:
                SlackClient().send_slack_direct_message(message, slack_username)
            else:
                # TODO no slack username found
                # they either dont have an account with this service
                # or their username is wrong
                print(
                    f"ERROR (send_slack_message_to_user): no slack username found: {github_username}"
                )

    def send_slack_message_to_channel(self, message, send_slack_message=True):
        if send_slack_message:
            SlackClient().send_slack_message_to_channel(message)
        else:
            print(message)

    def add_workflow_status_emoji(self, slack_message, payload):
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

    #
    # PARSING FUNCTIONS
    #
    def parse_pull_request(self, payload, send_slack_message=True):
        slack_message = ""

        merged = payload.get("pull_request", {}).get("merged")
        merged = str_to_bool(merged)

        action = payload.get("action")
        if action and action == "opened":
            slack_message = SlackClient.add_to_slack_string(
                slack_message, "PR opened! :tada:"
            )
        elif action and action == "closed":
            if merged:
                self.send_slack_message_to_user(
                    "Congrats! Your PR was merged! :tada:",
                    payload.get("pull_request", {}).get("user", {}).get("login"),
                )
                slack_message = SlackClient.add_to_slack_string(
                    slack_message, "PR merged! :merged_parrot:"
                )
            else:
                slack_message = SlackClient.add_to_slack_string(
                    slack_message, "PR closed! :sad:"
                )
        SlackClient.add_to_slack_string(slack_message, "action: {action}")

        title = payload.get("pull_request", {}).get("title")
        if title:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"title: {title}"
            )

        pr_number = payload.get("pull_request", {}).get("number")
        if pr_number:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"pr number: {pr_number}"
            )

        github_id = payload.get("pull_request", {}).get("id")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {github_id}"
        )
        state = payload.get("pull_request", {}).get("state")
        if state:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"state: {state}"
            )

        is_draft = payload.get("pull_request", {}).get("draft")
        is_draft = str_to_bool(is_draft)
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"draft: {is_draft}"
        )

        github_user = payload.get("pull_request", {}).get("user", {}).get("login")
        github_user_link = (
            payload.get("pull_request", {}).get("user", {}).get("html_url")
        )
        if github_user:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"user: {github_user}"
            )
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"user link: {github_user_link}"
            )

        repository = payload.get("repository", {}).get("full_name")
        repository_link = payload.get("repository", {}).get("html_url")
        if repository:
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"repository: {repository}"
            )
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"repository link: {repository_link}"
            )
        requested_reviewers = payload.get("pull_request", {}).get(
            "requested_reviewers", []
        )
        if requested_reviewers and len(requested_reviewers > 0):
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"requested reviewers: {requested_reviewers}"
            )
            # TODO send slack message to requested reviewers
        self.send_slack_message_to_channel(
            slack_message, send_slack_message=send_slack_message
        )
        
        # get or create pull request object
        pull_requests = GithubPullRequest.objects.filter(github_id=github_id)
        if pull_requests.count()  == 0:
            GithubPullRequest.objects.create(
                title=title,
                github_id=github_id,
                pr_number=pr_number,
                action=action,
                state=state,
                is_draft=is_draft,
                is_merged=merged,
                github_user=github_user,
                github_user_link=github_user_link,
                repository=repository,
                repository_link=repository_link,
                reviewers=requested_reviewers,
            )
        else:
            pull_requests.first().update(
                title=title,
                github_id=github_id,
                pr_number=pr_number,
                action=action,
                state=state,
                is_draft=is_draft,
                is_merged=merged,
                github_user=github_user,
                github_user_link=github_user_link,
                repository=repository,
                repository_link=repository_link,
                reviewers=requested_reviewers,
            )
            # TODO delete all other pr objects if there are any?
        
        return slack_message

    def parse_workflow_run(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        slack_message = self.add_workflow_status_emoji(slack_message, payload)

        github_id = payload.get('workflow_run', {}).get('id')
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {github_id}"
        )
        name = payload.get('workflow', {}).get('name')
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {name}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "webhook type: workflow run"
        )
        status = payload.get("workflow_run", {}).get("status")
        if status and status != "":
            slack_message = SlackClient.add_to_slack_string(
                slack_message,
                f"status: {status}",
            )
        conclusion = payload.get("workflow_run", {}).get("conclusion")
        if conclusion and conclusion != "":
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"conclusion: {conclusion}"
            )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"url: {payload.get('workflow', {}).get('html_url')}"
        )

        self.send_slack_message_to_channel(
            slack_message, send_slack_message=send_slack_message
        )
        
        # create or update workflow run object
        workflows = GithubWorkflow.objects.filter(github_id=github_id)
        if workflows.count() == 0:
            GithubWorkflow.objects.create(
                title=name,
                github_id=github_id,
                action=action,
                name=name,
                status=status,
                conclusion=conclusion,
                pull_request_github_id=payload.get("workflow_run", {}).get("pull_requests", [{}])[0].get("id"),
            )
        else:
            workflows.first().update(
                title=name,
                github_id=github_id,
                action=action,
                name=name,
                status=status,
                conclusion=conclusion,
                pull_request_github_id=payload.get("workflow_run", {}).get("pull_requests", [{}])[0].get("id"),
            )
        return slack_message

    def parse_workflow_job(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        slack_message = self.add_workflow_status_emoji(slack_message, payload)

        github_id = payload.get('workflow_job', {}).get('id')
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {github_id}"
        )
        name = payload.get('workflow_job', {}).get('name')
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {name}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "webhook type: workflow job"
        )
        status = payload.get("workflow_job", {}).get("status")
        if status and status != "":
            slack_message = SlackClient.add_to_slack_string(
                slack_message,
                f"status: {status}",
            )
        conclusion = payload.get("workflow_job", {}).get("conclusion")
        if conclusion and conclusion != "":
            slack_message = SlackClient.add_to_slack_string(
                slack_message, f"conclusion: {conclusion}"
            )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"url: {payload.get('workflow_job', {}).get('html_url')}",
        )

        self.send_slack_message_to_channel(
            slack_message, send_slack_message=send_slack_message
        )
        
        # create or update workflow job object
        workflows = GithubWorkflow.objects.filter(github_id=github_id)
        if workflows.count() == 0:
            GithubWorkflow.objects.create(
                title=name,
                github_id=github_id,
                action=action,
                name=name,
                status=status,
                conclusion=conclusion,
                pull_request_github_id=payload.get("workflow_job", {}).get("pull_requests", [{}])[0].get("id"),
            )
        else:
            workflows.first().update(
                title=name,
                github_id=github_id,
                action=action,
                name=name,
                status=status,
                conclusion=conclusion,
                pull_request_github_id=payload.get("workflow_job", {}).get("pull_requests", [{}])[0].get("id"),
            )
        return slack_message
