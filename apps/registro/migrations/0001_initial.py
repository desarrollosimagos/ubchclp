# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ubch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cod_estado', models.IntegerField()),
                ('cod_municipio', models.IntegerField(null=True)),
                ('cod_parroquia', models.IntegerField(null=True)),
                ('cod_ubch', models.IntegerField()),
                ('nom_ubch', models.CharField(max_length=200)),
                ('nac', models.CharField(default=b'V', max_length=1, verbose_name=b'Nacionalidad', choices=[(b'V', b'Venezolano'), (b'E', b'Extranjero')])),
                ('cedula', models.CharField(max_length=12, unique=True, null=True, verbose_name=b'C\xc3\xa9dula')),
                ('nombre', models.CharField(max_length=200, null=True, verbose_name=b'Nombres')),
                ('telefono', models.CharField(max_length=50)),
                ('cod_cargo', models.IntegerField()),
                ('cargo', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
