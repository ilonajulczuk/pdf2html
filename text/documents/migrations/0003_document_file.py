# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_document_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
