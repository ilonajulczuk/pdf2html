# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_document_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='pseudoid',
            field=models.CharField(blank=True, editable=False, max_length=16),
        ),
    ]
