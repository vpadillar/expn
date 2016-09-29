# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0011_pedido_tienda'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionTiempo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('retraso', models.FloatField(verbose_name=b'Retraso Motorizado', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('pedido', models.FloatField(verbose_name=b'Retraso Motorizado', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('distancia', models.FloatField(verbose_name=b'Distancia de pedido', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
    ]
