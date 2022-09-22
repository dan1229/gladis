from django.contrib import admin
from webhooks.models import WebhookReceived


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


admin.site.register(WebhookReceived, WebhookReceivedAdmin)
