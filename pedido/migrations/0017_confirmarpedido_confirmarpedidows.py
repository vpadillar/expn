# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0016_auto_20160627_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmarPedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('motorizado', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('pedido', models.ForeignKey(to='pedido.Pedido')),
            ],
            options={
                'verbose_name': 'Confirmacion',
                'verbose_name_plural': 'Confirmaciones',
            },
        ),
        migrations.CreateModel(
            name='ConfirmarPedidoWs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('motorizado', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('pedido', models.ForeignKey(to='pedido.PedidoWS')),
            ],
            options={
                'verbose_name': 'Confirmacion',
                'verbose_name_plural': 'Confirmaciones',
            },
        ),
    ]
