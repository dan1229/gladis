from django.contrib import admin
from webhooks.models import WebhookReceived, GithubWebhookReceived


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


admin.site.register(WebhookReceived, WebhookReceivedAdmin)
admin.site.register(GithubWebhookReceived, GithubWebhookReceivedAdmin)
