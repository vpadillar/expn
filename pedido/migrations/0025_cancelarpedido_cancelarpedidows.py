# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0024_auto_20160706_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelarPedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('pedido', models.ForeignKey(to='pedido.Pedido')),
            ],
            options={
                'verbose_name': 'Cancelar Pedido',
                'verbose_name_plural': 'Cancelaciones de Pedidos',
            },
        ),
        migrations.CreateModel(
            name='CancelarPedidoWs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('pedido', models.ForeignKey(to='pedido.PedidoWS')),
            ],
            options={
                'verbose_name': 'Cancelar PedidoWS',
                'verbose_name_plural': 'Cancelaciones de PedidoWS',
            },
        ),
    ]
