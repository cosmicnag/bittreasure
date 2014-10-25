# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0008_location_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasurehunt',
            name='m',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='treasurehunt',
            name='n',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
