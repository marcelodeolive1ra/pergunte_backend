# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0016_auto_20170124_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perguntarespondida',
            name='respostas',
            field=models.ManyToManyField(blank=True, null=True, to='pergunte.Alternativa', verbose_name='respostas'),
        ),
    ]
