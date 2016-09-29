# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_auto_20160716_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='token',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
