# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0009_auto_20160624_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='tienda',
        ),
    ]
