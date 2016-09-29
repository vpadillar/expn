# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_cliente_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='referencia',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
