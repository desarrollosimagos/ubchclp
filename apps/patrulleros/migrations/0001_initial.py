# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patrullero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula', models.IntegerField(unique=True)),
                ('p_nombre', models.CharField(max_length=50)),
                ('s_nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('p_apellido', models.CharField(max_length=50)),
                ('s_apellido', models.CharField(max_length=50, null=True, blank=True)),
                ('cedula_jefe', models.IntegerField()),
                ('twitter', models.CharField(max_length=50, null=True, blank=True)),
                ('telefono', models.CharField(max_length=11)),
                ('direccion', models.TextField(null=True, blank=True)),
                ('agregado', models.BooleanField(default=False)),
                ('estado', models.IntegerField(null=True, blank=True)),
                ('municipio', models.IntegerField(null=True, blank=True)),
                ('parroquia', models.IntegerField(null=True, blank=True)),
                ('cod_ubch_p', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
