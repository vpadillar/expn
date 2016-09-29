# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0020_configuraciontiempo_gps'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pedidows',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='configuraciontiempo',
            name='primer',
            field=models.IntegerField(verbose_name=b'Primer corte de quincena'),
        ),
        migrations.AlterField(
            model_name='configuraciontiempo',
            name='segundo',
            field=models.IntegerField(verbose_name=b'Segundo corte de quincena'),
        ),
    ]
