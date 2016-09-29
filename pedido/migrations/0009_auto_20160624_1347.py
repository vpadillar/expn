# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
        ('pedido', '0008_auto_20160623_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidows',
            name='empresa',
            field=models.ForeignKey(blank=True, to='usuario.Empresa', null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tienda',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedidows',
            name='tienda',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
