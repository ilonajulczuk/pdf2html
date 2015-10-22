# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20151022_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='html',
            field=models.TextField(null=True),
        ),
    ]
