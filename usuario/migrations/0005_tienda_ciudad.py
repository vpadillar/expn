# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_tienda_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='ciudad',
            field=models.ForeignKey(default=1, to='usuario.Ciudad'),
            preserve_default=False,
        ),
    ]
