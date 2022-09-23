from django.contrib import admin
from webhooks.models import WebhookReceived, GithubWebhookReceived, GithubPullRequest, GithubWorkflow


class WebhookReceivedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "received_at",
    )
    search_fields = (
        "id",
        "sender",
        "received_at",
        "payload",
    )
    readonly_fields = ("id",)
    list_per_page = 100


class GithubWebhookReceivedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "action",
        "webhook_type",
        "received_at",
    )
    search_fields = (
        "id",
        "sender",
        "action",
        "webhook_type",
        "received_at",
        "payload",
    )
    readonly_fields = ("id",)
    list_per_page = 100

class GithubPullRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pr_number",
        "repository",
        "github_user",
        "state",
        "is_merged",
        "is_draft",
        "datetime_created",
    )
    search_fields = (
        "title",
        "pr_number",
        "repository",
        "github_user",
        "state",
        "is_merged",
        "is_draft",
        "datetime_created",
    )
    readonly_fields = ("id",)
    list_per_page = 100

class GithubWorkflowAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "github_id",
        "name",
        "action",
        "status",
        "conclusion",
        "pull_request_github_id",
        "datetime_created",
    )
    search_fields = (
        "title",
        "github_id",
        "name",
        "action",
        "status",
        "conclusion",
        "pull_request_github_id",
        "datetime_created",
    )
    readonly_fields = ("id",)
    list_per_page = 100
    
    
admin.site.register(WebhookReceived, WebhookReceivedAdmin)
admin.site.register(GithubWebhookReceived, GithubWebhookReceivedAdmin)
admin.site.register(GithubPullRequest, GithubPullRequestAdmin)
admin.site.register(GithubWorkflow, GithubWorkflowAdmin)
