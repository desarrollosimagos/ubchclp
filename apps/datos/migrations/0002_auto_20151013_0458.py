# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos',
            name='telefono',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
