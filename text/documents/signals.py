from documents.models import Document
from documents.tasks import convert_to_html
from django.db.models.signals import post_save


def process_document(sender, instance, created, **kwargs):
    if created:
        convert_to_html.delay(instance.pk)


post_save.connect(process_document, sender=Document, dispatch_uid="process_document")
