# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0021_auto_20160706_0119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='estado',
            new_name='activado',
        ),
        migrations.AddField(
            model_name='pedido',
            name='reactivacion',
            field=models.BooleanField(default=False),
        ),
    ]
