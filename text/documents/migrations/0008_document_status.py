# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_document_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
