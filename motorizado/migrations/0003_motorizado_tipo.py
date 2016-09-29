# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motorizado', '0002_auto_20160605_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorizado',
            name='tipo',
            field=models.IntegerField(default=1, choices=[(1, b'Planta'), (2, b'Suscrito')]),
            preserve_default=False,
        ),
    ]
