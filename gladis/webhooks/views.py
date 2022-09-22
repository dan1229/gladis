import json

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

from webhooks.models import WebhookReceived


@csrf_exempt
@require_POST
@non_atomic_requests
def github_webhook(request):
    payload = json.loads(request.body)
    WebhookReceived.objects.create(
        received_at=timezone.now(),
        sender="github",
        payload=payload,
    )
    process_webhook_payload(payload)
    return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    print(payload)
    # TODO
