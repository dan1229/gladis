from webhooks.slack import SlackClient

from core.helpers import str_to_bool


class GithubParser:
    
    def send_slack_message_to_user(self, message, github_username, send_slack_message=True):
        if send_slack_message:
            SlackClient().send_slack_direct_message(message, SlackClient.get_slack_username(github_username))
            
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
                self.send_slack_message_to_user("Congrats! Your PR was merged! :tada:", payload.get("pull_request", {}).get("user", {}).get("login"))
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


        # TODO
        # save reviewer and author info
        # handle if switching base branch notification?

        self.send_slack_message_to_channel(slack_message, send_slack_message=send_slack_message)
        return slack_message

    def parse_workflow_run(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        slack_message = self.add_workflow_status_emoji(slack_message, payload)

        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {payload.get('workflow_run', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {payload.get('workflow', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "webhook type: workflow run"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"status: {payload.get('workflow_run', {}).get('status')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"conclusion: {payload.get('workflow_run', {}).get('conclusion')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"url: {payload.get('workflow', {}).get('html_url')}"
        )

        self.send_slack_message_to_channel(slack_message, send_slack_message=send_slack_message)
        return slack_message

    def parse_workflow_job(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"Workflow {action}"
        )
        slack_message = self.add_workflow_status_emoji(slack_message, payload)

        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"id: {payload.get('workflow_job', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {payload.get('workflow_job', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, "webhook type: workflow job"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"status: {payload.get('workflow_job', {}).get('status')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"conclusion: {payload.get('workflow_run', {}).get('conclusion')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"url: {payload.get('workflow_job', {}).get('html_url')}",
        )

        self.send_slack_message_to_channel(slack_message, send_slack_message=send_slack_message)
        return slack_message
