# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0002_auto_20170111_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1, verbose_name='Alternativa')),
                ('textoResposta', models.TextField(verbose_name='Texto da Resposta')),
                ('alternativaCorreta', models.BooleanField(verbose_name='Alternativa correta?')),
            ],
            options={
                'verbose_name': 'Resposta',
                'verbose_name_plural': 'Respostas',
            },
        ),
        migrations.AlterModelOptions(
            name='aluno',
            options={'verbose_name': 'Aluno', 'verbose_name_plural': 'Alunos'},
        ),
        migrations.AlterModelOptions(
            name='materia',
            options={'verbose_name': 'Matéria', 'verbose_name_plural': 'Matérias'},
        ),
        migrations.AlterModelOptions(
            name='pergunta',
            options={'verbose_name': 'Pergunta', 'verbose_name_plural': 'Perguntas'},
        ),
        migrations.AlterModelOptions(
            name='pessoa',
            options={'verbose_name': 'Pessoa', 'verbose_name_plural': 'Pessoas'},
        ),
        migrations.AlterModelOptions(
            name='professor',
            options={'verbose_name': 'Professor', 'verbose_name_plural': 'Professores'},
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='respostaCorreta',
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='respostas',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='curso',
            field=models.CharField(max_length=100, verbose_name='Curso'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='ano',
            field=models.IntegerField(verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='codigoInscricao',
            field=models.CharField(max_length=30, unique=True, verbose_name='Código de Inscrição'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='nomeDisciplina',
            field=models.CharField(max_length=200, verbose_name='Nome da disciplina'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='semestre',
            field=models.IntegerField(verbose_name='Semestre'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='codigo',
            field=models.IntegerField(unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='disponivel',
            field=models.BooleanField(verbose_name='Pergunta disponível?'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='pergunta',
            field=models.TextField(verbose_name='Texto da Pergunta'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='sobrenome',
            field=models.CharField(max_length=100, verbose_name='Sobrenome'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='universidade',
            field=models.CharField(max_length=100, verbose_name='Universidade'),
        ),
        migrations.DeleteModel(
            name='Resposta',
        ),
        migrations.AddField(
            model_name='pergunta',
            name='alternativas',
            field=models.ManyToManyField(to='pergunte.Alternativa', verbose_name='Alternativas'),
        ),
    ]
