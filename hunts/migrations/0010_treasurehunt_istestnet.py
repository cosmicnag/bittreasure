# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0009_auto_20141025_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasurehunt',
            name='istestnet',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
