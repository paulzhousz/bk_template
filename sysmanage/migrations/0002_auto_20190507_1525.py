# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmanage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='operated_object',
            field=models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u5bf9\u8c61', blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='operated_type',
            field=models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u7c7b\u578b', blank=True),
        ),
    ]
