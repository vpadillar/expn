# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0023_auto_20160706_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidows',
            old_name='estado',
            new_name='activado',
        ),
    ]
