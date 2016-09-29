# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
                ('placa', models.CharField(unique=True, max_length=6)),
                ('t_propiedad', models.CharField(unique=True, max_length=50, verbose_name=b'Tarjeta de Propiedad')),
                ('estado', models.BooleanField(default=True)),
                ('empresaM', models.ForeignKey(to='usuario.Empresa')),
            ],
            options={
                'verbose_name': 'Moto',
                'verbose_name_plural': 'Motos',
            },
        ),
        migrations.CreateModel(
            name='Motorizado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('licencia', models.CharField(unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'licencia no valida', b'invalid')])),
                ('identifier', models.CharField(unique=True, max_length=20)),
                ('empleado', models.OneToOneField(to='usuario.Empleado')),
                ('moto', models.OneToOneField(to='motorizado.Moto')),
            ],
            options={
                'verbose_name': 'Motorizado',
                'verbose_name_plural': 'Motorizados',
            },
        ),
        migrations.CreateModel(
            name='Soat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numeroS', models.CharField(unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'numero no valida', b'invalid')])),
                ('fecha_expedicionS', models.DateField()),
                ('fecha_expiracionS', models.DateField()),
            ],
            options={
                'verbose_name': 'Soat',
                'verbose_name_plural': 'Soats',
            },
        ),
        migrations.CreateModel(
            name='Tecno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numeroT', models.CharField(unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'numero no valida', b'invalid')])),
                ('fecha_expedicionT', models.DateField()),
                ('fecha_expiracionT', models.DateField()),
            ],
            options={
                'verbose_name': 'Tecnomecanica',
                'verbose_name_plural': 'Tecnomecanicas',
            },
        ),
        migrations.AddField(
            model_name='moto',
            name='soat',
            field=models.OneToOneField(to='motorizado.Soat'),
        ),
        migrations.AddField(
            model_name='moto',
            name='tecno',
            field=models.OneToOneField(to='motorizado.Tecno'),
        ),
    ]
