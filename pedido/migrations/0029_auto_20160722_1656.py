# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0028_logenvio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logenvio',
            old_name='empresa',
            new_name='tienda',
        ),
    ]
