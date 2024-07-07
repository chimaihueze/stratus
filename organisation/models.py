import uuid

from django.db import models


class Organisation(models.Model):
    orgId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=120)
