# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0030_auto_20160722_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='logenvio',
            name='data',
            field=models.CharField(default=1, max_length=100000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logenvio',
            name='response',
            field=models.CharField(max_length=10000),
        ),
    ]
