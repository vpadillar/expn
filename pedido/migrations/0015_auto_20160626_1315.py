# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0014_auto_20160626_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidows',
            name='detalle',
            field=models.CharField(max_length=10000, null=True, blank=True),
        ),
    ]
