from django.db import models

class Alternativa(models.Model):
    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __str__(self):
        return '[' + self.letra + '] ' + self.textoResposta

    letra = models.CharField(max_length=1, verbose_name='Alternativa')
    textoResposta = models.TextField(verbose_name='Texto da Alternativa')
    alternativaCorreta = models.BooleanField(verbose_name='Alternativa correta?')


class Pergunta(models.Model):
    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return self.pergunta

    pergunta = models.TextField(verbose_name='Texto da Pergunta')
    alternativas = models.ManyToManyField(Alternativa, verbose_name='Alternativas')
    disponivel = models.BooleanField(verbose_name='Pergunta disponível?')


class Pessoa(models.Model):
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    nome = models.CharField(max_length=50, verbose_name='Nome')
    sobrenome = models.CharField(max_length=100, verbose_name='Sobrenome')
    email = models.EmailField(verbose_name='E-mail')


class Professor(Pessoa):
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return '[Professor] ' + self.nome + ' ' + self.sobrenome

    universidade = models.CharField(max_length=100, verbose_name='Universidade')


class Materia(models.Model):
    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'

    def __str__(self):
        return self.nomeDisciplina + ' (' + str(self.ano) + '/' + str(self.semestre) + ')'

    ano = models.IntegerField(verbose_name='Ano')
    semestre = models.IntegerField(verbose_name='Semestre')
    turma = models.CharField(max_length=1, verbose_name='Turma')
    nomeDisciplina = models.CharField(max_length=200, verbose_name='Nome da disciplina')
    codigoInscricao = models.CharField(max_length=30, verbose_name='Código de inscrição', unique=True)
    professor = models.ForeignKey(Professor, verbose_name='Professor(a)')
    perguntas = models.ManyToManyField(Pergunta, verbose_name='Perguntas', blank=True)


class Aluno(Pessoa):
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return '[Aluno] ' + self.nome + ' ' + self.sobrenome

    curso = models.CharField(max_length=100, verbose_name='Curso')
    materias = models.ManyToManyField(Materia, verbose_name='Matérias inscritas', blank=True)
