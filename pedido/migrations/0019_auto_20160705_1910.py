# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_tienda_url'),
        ('pedido', '0018_auto_20160630_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuraciontiempo',
            name='empresa',
            field=models.ForeignKey(default=1, to='usuario.Empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciontiempo',
            name='primer',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciontiempo',
            name='segundo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
