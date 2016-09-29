# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0022_auto_20160706_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuraciontiempo',
            old_name='primer',
            new_name='primero',
        ),
    ]
