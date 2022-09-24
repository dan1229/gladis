from django.db import models

from core.models import AbstractBaseModel


#
# GITHUB PULL REQUEST ====================================== #
#
class GithubPullRequest(AbstractBaseModel):
    title = models.CharField(max_length=255, help_text="The title of the PR.")
    github_id = models.CharField(max_length=255, help_text="The id of the workflow.")

    pr_number = models.IntegerField(help_text="The number of the PR.")
    action = models.CharField(max_length=255, help_text="The action of the PR.")
    state = models.CharField(max_length=255, help_text="The state of the PR.")

    is_draft = models.BooleanField(default=False, help_text="Is the PR a draft?")
    is_merged = models.BooleanField(default=False, help_text="Is the PR merged?")

    github_user = models.CharField(max_length=255, help_text="The user of the PR.")
    github_user_link = models.CharField(
        max_length=255, help_text="The user link of the PR."
    )
    repository = models.CharField(max_length=255, help_text="The repository of the PR.")
    repository_link = models.CharField(
        max_length=255, help_text="The repository link of the PR."
    )

    reviewers = models.JSONField(default=None, null=True)

    class Meta:
        ordering = ["datetime_created"]

    def __str__(self):
        return f"PR #{self.pr_number}: {self.title} by {self.github_user}"


#
# GITHUB WORKFLOW ====================================== #
#
class GithubWorkflow(AbstractBaseModel):
    title = models.CharField(
        max_length=255, help_text="The title of the workflow."
    )  # this may be redundant, i.e., 'title' is the same as 'name'
    github_id = models.CharField(max_length=255, help_text="The ID of the workflow.")

    action = models.CharField(max_length=255, help_text="The action of the workflow.")
    name = models.CharField(max_length=255, help_text="The name of the workflow.")
    status = models.CharField(max_length=255, help_text="The status of the PR.")
    conclusion = models.CharField(max_length=255, help_text="The conclusion of the PR.")
    pull_request_github_id = models.CharField(
        max_length=255, help_text="The ID of the PR."
    )

    class Meta:
        ordering = ["datetime_created"]

    def __str__(self):
        return f"Workflow #{self.github_id}: {self.name} - {self.conclusion}"
