# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
        ('pedido', '0010_remove_pedido_tienda'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='tienda',
            field=models.ForeignKey(default=3, to='usuario.Tienda'),
            preserve_default=False,
        ),
    ]
