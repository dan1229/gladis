import uuid

from django.db import models

"""
# ==================================================================================== #
# ABSTRACT BASE MODEL ================================================================ #
# ==================================================================================== #
"""
#
# ABSTRACT BASE MODEL =================================== #
# handles all shared functionality between classes
#


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "Abstract Base Model"
