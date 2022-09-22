from django.db import models

from core.models import AbstractBaseModel

# Create your models here.

#
# WEBHOOK RECEIVED ====================================== #
#
class WebhookReceived(AbstractBaseModel):
    received_at = models.DateTimeField(help_text="When we received the event.")
    sender = models.CharField(max_length=255, help_text="The sender of the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]
        
    def __str__(self):
        return f"Webhook Received: {self.received_at}"