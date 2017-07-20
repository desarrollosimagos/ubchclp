# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institucion', models.TextField()),
                ('cedula_representante', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=11)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
