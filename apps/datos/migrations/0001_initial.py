# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula', models.IntegerField(unique=True)),
                ('p_nombre', models.CharField(max_length=50)),
                ('s_nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('p_apellido', models.CharField(max_length=50)),
                ('s_apellido', models.CharField(max_length=50, null=True, blank=True)),
                ('cargo', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_naci', models.DateTimeField(null=True)),
                ('telefono', models.CharField(max_length=11)),
                ('estatus', models.CharField(max_length=11)),
                ('fecha_ingreso', models.DateTimeField(null=True)),
                ('tipo_empledo', models.CharField(max_length=20)),
                ('departamento', models.TextField(null=True, blank=True)),
                ('estado', models.IntegerField(null=True, blank=True)),
                ('municipio', models.IntegerField(null=True, blank=True)),
                ('parroquia', models.IntegerField(null=True, blank=True)),
                ('direccion', models.TextField(null=True, blank=True)),
                ('twitter', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
