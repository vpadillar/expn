# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
        ('pedido', '0013_auto_20160626_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidows',
            name='detalle',
            field=models.CharField(default=3, max_length=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidows',
            name='tienda',
            field=models.ForeignKey(default=3, to='usuario.Tienda'),
            preserve_default=False,
        ),
    ]
