import string
import random

from django_enumfield import enum
from django.db import models, IntegrityError
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
    pseudoid = models.CharField(max_length=16, blank=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = enum.EnumField(DocumentStatus, default=DocumentStatus.PENDING)

    def save(self, *args, **kwargs):
        if not self.pseudoid:
            self.pseudoid = generate_random_alphanumeric(16)
            # using your function as above or anything else
        success = False
        failures = 0
        while not success:
            try:
                super(Document, self).save(*args, **kwargs)
            except IntegrityError:
                failures += 1
                if failures > 5:  # or some other arbitrary cutoff point at which things are clearly wrong
                    raise
                else:
                    # looks like a collision, try another random value
                    self.pseudoid = generate_random_alphanumeric(16)
            else:
                 success = True

class Image(models.Model):
    img = models.ImageField(null=True)
    document = models.ForeignKey(Document)


def generate_random_alphanumeric(size=16, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))