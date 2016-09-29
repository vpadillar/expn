# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0019_auto_20160705_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuraciontiempo',
            name='gps',
            field=models.FloatField(default=1, verbose_name=b'Gps de Motorizado (Min)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
    ]
