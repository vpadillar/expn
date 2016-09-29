# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
        ('pedido', '0007_remove_pedidows_tienda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidows',
            name='empresa',
        ),
        migrations.AddField(
            model_name='pedidows',
            name='tienda',
            field=models.ForeignKey(blank=True, to='usuario.Tienda', null=True),
        ),
    ]
