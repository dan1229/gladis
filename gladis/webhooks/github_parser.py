from webhooks.models.github import GithubPullRequest, GithubWorkflow


class GithubParser:

    #
    # PARSING FUNCTIONS
    #
    def parse_pull_request(self, payload):
        merged = payload.get("pull_request", {}).get("merged")
        action = payload.get("action")
        title = payload.get("pull_request", {}).get("title")
        pr_number = payload.get("pull_request", {}).get("number")
        github_id = payload.get("pull_request", {}).get("id")
        state = payload.get("pull_request", {}).get("state")
        is_draft = payload.get("pull_request", {}).get("draft")
        github_user = payload.get("pull_request", {}).get("user", {}).get("login")
        github_user_link = (
            payload.get("pull_request", {}).get("user", {}).get("html_url")
        )
        repository = payload.get("repository", {}).get("full_name")
        repository_link = payload.get("repository", {}).get("html_url")
        requested_reviewers = payload.get("pull_request", {}).get(
            "requested_reviewers", []
        )
        pull_request_url = payload.get("pull_request", {}).get("html_url")

        # get or create pull request object
        pull_requests = GithubPullRequest.objects.filter(github_id=github_id)
        if pull_requests.count() == 0:
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
                pull_request_url=pull_request_url,
            )
        else:
            pull_request = pull_requests.first()
            # TODO delete all other pr objects if there are any?
            pull_request.title = title
            pull_request.github_id = github_id
            pull_request.pr_number = pr_number
            pull_request.action = action
            pull_request.state = state
            pull_request.is_draft = is_draft
            pull_request.is_merged = merged
            pull_request.github_user = github_user
            pull_request.github_user_link = github_user_link
            pull_request.repository = repository
            pull_request.repository_link = repository_link
            pull_request.reviewers = requested_reviewers
            pull_request.pull_request_url = pull_request_url

    def parse_workflow_run(self, payload):
        action = payload.get("action")
        github_id = payload.get("workflow_run", {}).get("id")
        name = payload.get("workflow", {}).get("name")
        status = payload.get("workflow_run", {}).get("status")
        conclusion = payload.get("workflow_run", {}).get("conclusion")
        workflow_url = payload.get("workflow", {}).get("html_url")
        pull_request_url = (
            payload.get("workflow_run", {}).get("pull_requests")[0].get("url")
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
                pull_request_github_id=payload.get("workflow_run", {})
                .get("pull_requests", [{}])[0]
                .get("id"),
                workflow_url=workflow_url,
                pull_request_url=pull_request_url,
            )
        else:
            workflow = workflows.first()
            workflow.title = name
            workflow.github_id = github_id
            workflow.action = action
            workflow.name = name
            workflow.status = status
            workflow.conclusion = conclusion
            workflow.pull_request_github_id = (
                payload.get("workflow_run", {}).get("pull_requests", [{}])[0].get("id")
            )
            workflow.workflow_url = workflow_url
            workflow.pull_request_url = pull_request_url

    def parse_workflow_job(self, payload):
        action = payload.get("action")
        github_id = payload.get("workflow_run", {}).get("id")
        name = payload.get("workflow", {}).get("name")
        status = payload.get("workflow_run", {}).get("status")
        conclusion = payload.get("workflow_run", {}).get("conclusion")
        workflow_url = payload.get("workflow", {}).get("html_url")
        pull_request_url = (
            payload.get("workflow_run", {}).get("pull_requests")[0].get("url")
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
                pull_request_github_id=payload.get("workflow_job", {})
                .get("pull_requests", [{}])[0]
                .get("id"),
                workflow_url=workflow_url,
                pull_request_url=pull_request_url,
            )
        else:
            workflow = workflows.first()
            workflow.title = name
            workflow.github_id = github_id
            workflow.action = action
            workflow.name = name
            workflow.status = status
            workflow.conclusion = conclusion
            workflow.pull_request_github_id = (
                payload.get("workflow_run", {}).get("pull_requests", [{}])[0].get("id")
            )
            workflow.workflow_url = workflow_url
            workflow.pull_request_url = pull_request_url
