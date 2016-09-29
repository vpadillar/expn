# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0015_auto_20160626_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedidows',
            options={'verbose_name': 'PedidoWs', 'verbose_name_plural': 'PedidosWs'},
        ),
        migrations.AddField(
            model_name='pedido',
            name='notificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='time',
            name='notificado',
            field=models.DateTimeField(null=True),
        ),
    ]
