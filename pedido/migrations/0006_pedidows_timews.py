# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
        ('pedido', '0005_auto_20160623_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoWS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_pedido', models.CharField(max_length=50)),
                ('npedido_express', models.CharField(max_length=50)),
                ('fecha_pedido', models.DateField(auto_now=True)),
                ('tienda', models.CharField(max_length=50, null=True, blank=True)),
                ('cliente', models.CharField(max_length=300, null=True, blank=True)),
                ('tipo_pago', models.CharField(max_length=50)),
                ('observacion', models.TextField(max_length=200, null=True, blank=True)),
                ('total', models.DecimalField(null=True, max_digits=20, decimal_places=2)),
                ('entregado', models.BooleanField(default=False)),
                ('despachado', models.BooleanField(default=False)),
                ('confirmado', models.BooleanField(default=False)),
                ('alistado', models.BooleanField(default=False)),
                ('items', models.CharField(max_length=2000, null=True, blank=True)),
                ('alistador', models.ForeignKey(related_name='alistadorws', to='usuario.Empleado', null=True)),
                ('empresa', models.ForeignKey(blank=True, to='usuario.Empresa', null=True)),
                ('motorizado', models.ForeignKey(related_name='motorizado_enviadows', to='usuario.Empleado', null=True)),
                ('supervisor', models.ForeignKey(related_name='supervisorws', to='usuario.Empleado', null=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='TimeWS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado', models.DateTimeField()),
                ('confirmado', models.DateTimeField(null=True)),
                ('alistado', models.DateTimeField(null=True)),
                ('despachado', models.DateTimeField(null=True)),
                ('entregado', models.DateTimeField(null=True)),
                ('pedido', models.OneToOneField(to='pedido.PedidoWS')),
            ],
        ),
    ]
