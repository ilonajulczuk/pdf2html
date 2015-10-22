from django_enumfield import enum
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class DocumentStatus(enum.Enum):
    PENDING = 1
    STARTED = 2
    ERROR = 3
    DONE = 4

    labels = {
        PENDING: 'Pending',
        STARTED: 'Started',
        ERROR: 'Error',
        DONE: 'Done',
    }

    _transitions = {
        STARTED: (PENDING,),
        DONE: (STARTED,),
        ERROR: (STARTED,),
    }


class Document(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.FileField()
    html = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = enum.EnumField(DocumentStatus, default=DocumentStatus.PENDING)


class Image(models.Model):
    img = models.ImageField(null=True)
    document = models.ForeignKey(Document)
