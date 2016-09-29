# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_auto_20160702_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
