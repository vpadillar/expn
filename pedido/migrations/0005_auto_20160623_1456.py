# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_punto_seguimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidows',
            name='alistador',
        ),
        migrations.RemoveField(
            model_name='pedidows',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='pedidows',
            name='motorizado',
        ),
        migrations.RemoveField(
            model_name='pedidows',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='timews',
            name='pedido',
        ),
        migrations.DeleteModel(
            name='PedidoWS',
        ),
        migrations.DeleteModel(
            name='TimeWS',
        ),
    ]
