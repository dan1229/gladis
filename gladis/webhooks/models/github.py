from django.db import models

from core.models import AbstractBaseModel


#
# GITHUB PULL REQUEST ====================================== #
#
class GithubPullRequest(AbstractBaseModel):
    title = models.CharField(
        max_length=255, help_text="The title of the PR.", blank=True, null=True
    )
    github_id = models.CharField(
        max_length=255, help_text="The id of the workflow.", blank=True, null=True
    )

    pr_number = models.IntegerField(
        help_text="The number of the PR.", blank=True, null=True
    )
    state = models.CharField(
        max_length=255, help_text="The state of the PR.", blank=True, null=True
    )

    is_draft = models.BooleanField(
        default=False, help_text="Is the PR a draft?", blank=True, null=True
    )
    is_merged = models.BooleanField(
        default=False, help_text="Is the PR merged?", blank=True, null=True
    )

    github_user = models.CharField(
        max_length=255, help_text="The user of the PR.", blank=True, null=True
    )
    github_user_link = models.CharField(
        max_length=255, help_text="The user link of the PR.", blank=True, null=True
    )
    repository = models.CharField(
        max_length=255, help_text="The repository of the PR.", blank=True, null=True
    )
    repository_link = models.CharField(
        max_length=255,
        help_text="The repository link of the PR.",
        blank=True,
        null=True,
    )

    reviewers = models.JSONField(default=None, null=True)
    pull_request_url = models.CharField(
        max_length=255, help_text="The link of the PR.", blank=True, null=True
    )

    class Meta:
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"PR #{self.pr_number}: {self.title} by {self.github_user}"


#
# GITHUB WORKFLOW ====================================== #
#
class GithubWorkflow(AbstractBaseModel):
    name = models.CharField(
        max_length=255, help_text="The name of the workflow.", blank=True, null=True
    )
    github_id = models.CharField(
        max_length=255, help_text="The ID of the workflow.", blank=True, null=True
    )
    github_user = models.CharField(
        max_length=255, help_text="The user of the PR.", blank=True, null=True
    )
    github_user_link = models.CharField(
        max_length=255, help_text="The user link of the PR.", blank=True, null=True
    )
    action = models.CharField(
        max_length=255, help_text="The action of the workflow.", blank=True, null=True
    )
    status = models.CharField(
        max_length=255, help_text="The status of the PR.", blank=True, null=True
    )
    conclusion = models.CharField(
        max_length=255, help_text="The conclusion of the PR.", blank=True, null=True
    )
    pull_request_github_id = models.CharField(
        max_length=255, help_text="The ID of the PR.", blank=True, null=True
    )
    pull_request_url = models.CharField(
        max_length=255, help_text="The URL of the PR.", blank=True, null=True
    )
    workflow_url = models.CharField(
        max_length=255, help_text="The URL of the workflow.", blank=True, null=True
    )

    class Meta:
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"Workflow #{self.github_id}: {self.name} - {self.conclusion}"
