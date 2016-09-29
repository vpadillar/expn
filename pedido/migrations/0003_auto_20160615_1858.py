# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_auto_20160607_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemspedido',
            name='cantidad',
            field=models.DecimalField(max_digits=20, decimal_places=2, validators=[django.core.validators.RegexValidator(re.compile(b'^[1-9][0-9]*$'), b'numero no valida', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='itemspedido',
            name='valor_unitario',
            field=models.DecimalField(max_digits=20, decimal_places=2, validators=[django.core.validators.RegexValidator(re.compile(b'^[1-9][0-9]*$'), b'numero no valida', b'invalid')]),
        ),
    ]
