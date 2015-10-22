# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='img',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
