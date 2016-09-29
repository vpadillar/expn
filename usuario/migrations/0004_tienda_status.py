# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_tienda_referencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
