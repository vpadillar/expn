# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_tienda_ciudad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
