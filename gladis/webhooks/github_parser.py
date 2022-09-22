from webhooks.slack import SlackClient


class GithubParser():
    
    def send_slack_message(self, send_slack_message, message):
        if send_slack_message:
            SlackClient().send_slack_message(message)
        else:
            print(message)

    #
    # PARSING FUNCTIONS
    #
    def parse_pull_request(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
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

        merged = payload.get("pull_request", {}).get("merged")
        merged = str_to_bool(merged)
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"merged: {merged}"
        )

        # TODO
        # save reviewer and author info
        # handle if switching base branch notification?

        self.send_slack_message(send_slack_message, slack_message)
        return slack_message

    def parse_workflow_run(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
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
            slack_message, f"id: {payload.get('workflow_run', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {payload.get('workflow', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"state: {payload.get('workflow_run', {}).get('state')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"url: {payload.get('workflow', {}).get('html_url')}"
        )
        
        self.send_slack_message(send_slack_message, slack_message)
        return slack_message

    def parse_workflow_job(self, payload, send_slack_message=True):
        slack_message = ""

        action = payload.get("action")
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
            slack_message, f"id: {payload.get('workflow_job', {}).get('id')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message, f"name: {payload.get('workflow_job', {}).get('name')}"
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"state: {payload.get('workflow_job', {}).get('state')}",
        )
        slack_message = SlackClient.add_to_slack_string(
            slack_message,
            f"url: {payload.get('workflow_job', {}).get('html_url')}",
        )

        self.send_slack_message(send_slack_message, slack_message)
        return slack_message
