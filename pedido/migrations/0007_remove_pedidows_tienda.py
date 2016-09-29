# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0006_pedidows_timews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidows',
            name='tienda',
        ),
    ]
