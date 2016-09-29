# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0012_configuraciontiempo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidows',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='pedidows',
            name='tienda',
        ),
        migrations.AlterField(
            model_name='configuraciontiempo',
            name='distancia',
            field=models.FloatField(verbose_name=b'Distancia de pedido (Mts)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='configuraciontiempo',
            name='pedido',
            field=models.FloatField(verbose_name=b'Asignacion de Pedido (Min)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='configuraciontiempo',
            name='retraso',
            field=models.FloatField(verbose_name=b'Retraso de Motorizado (Min)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
