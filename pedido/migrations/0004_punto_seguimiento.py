# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_auto_20160615_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Punto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pedido', models.ForeignKey(blank=True, to='pedido.Pedido', null=True)),
                ('ruta', models.ManyToManyField(to='pedido.Punto')),
            ],
        ),
    ]
