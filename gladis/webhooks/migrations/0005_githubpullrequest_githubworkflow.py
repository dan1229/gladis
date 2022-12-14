# Generated by Django 4.1.1 on 2022-09-23 20:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("webhooks", "0004_alter_githubwebhookreceived_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="GithubPullRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(help_text="The title of the PR.", max_length=255),
                ),
                (
                    "github_id",
                    models.CharField(
                        help_text="The id of the workflow.", max_length=255
                    ),
                ),
                ("pr_number", models.IntegerField(help_text="The number of the PR.")),
                (
                    "action",
                    models.CharField(help_text="The action of the PR.", max_length=255),
                ),
                (
                    "state",
                    models.CharField(help_text="The state of the PR.", max_length=255),
                ),
                (
                    "is_draft",
                    models.BooleanField(default=False, help_text="Is the PR a draft?"),
                ),
                (
                    "is_merged",
                    models.BooleanField(default=False, help_text="Is the PR merged?"),
                ),
                (
                    "github_user",
                    models.CharField(help_text="The user of the PR.", max_length=255),
                ),
                (
                    "github_user_link",
                    models.CharField(
                        help_text="The user link of the PR.", max_length=255
                    ),
                ),
                (
                    "repository",
                    models.CharField(
                        help_text="The repository of the PR.", max_length=255
                    ),
                ),
                (
                    "repository_link",
                    models.CharField(
                        help_text="The repository link of the PR.", max_length=255
                    ),
                ),
                ("reviewers", models.JSONField(default=None, null=True)),
            ],
            options={
                "ordering": ["datetime_created"],
            },
        ),
        migrations.CreateModel(
            name="GithubWorkflow",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(
                        help_text="The title of the workflow.", max_length=255
                    ),
                ),
                (
                    "github_id",
                    models.CharField(
                        help_text="The ID of the workflow.", max_length=255
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        help_text="The action of the workflow.", max_length=255
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of the workflow.", max_length=255
                    ),
                ),
                (
                    "status",
                    models.CharField(help_text="The status of the PR.", max_length=255),
                ),
                (
                    "conclusion",
                    models.CharField(
                        help_text="The conclusion of the PR.", max_length=255
                    ),
                ),
                (
                    "pull_request_github_id",
                    models.CharField(help_text="The ID of the PR.", max_length=255),
                ),
            ],
            options={
                "ordering": ["datetime_created"],
            },
        ),
    ]
