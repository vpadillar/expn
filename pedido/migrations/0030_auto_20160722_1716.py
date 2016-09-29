# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0029_auto_20160722_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logenvio',
            name='response',
            field=models.CharField(max_length=100000),
        ),
    ]
