# Generated by Django 4.1.1 on 2022-09-22 15:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WebhookReceived",
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
                    "received_at",
                    models.DateTimeField(help_text="When we received the event."),
                ),
                ("payload", models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name="webhookreceived",
            index=models.Index(
                fields=["received_at"], name="webhooks_we_receive_34397a_idx"
            ),
        ),
    ]
