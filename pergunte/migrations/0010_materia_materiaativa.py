# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0009_materia_turma'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='materiaAtiva',
            field=models.BooleanField(default=True, verbose_name='Matéria ativa?'),
        ),
    ]
