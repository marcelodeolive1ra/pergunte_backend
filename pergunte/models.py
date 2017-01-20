from django.db import models

class Alternativa(models.Model):
    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __str__(self):
        return '[' + self.letra + '] ' + self.textoResposta

    letra = models.CharField(max_length=1, verbose_name='alternativa')
    textoAlternativa = models.TextField(verbose_name='texto da alternativa', blank=True)


class Pergunta(models.Model):
    class Meta:
        verbose_name = 'pergunta'
        verbose_name_plural = 'perguntas'

    texto_pergunta = models.TextField(verbose_name='texto da pergunta', blank=True)
    alternativas = models.ManyToManyField(Alternativa, verbose_name='alternativas')
    disponivel = models.BooleanField(verbose_name='pergunta disponível?')


class Pessoa(models.Model):
    class Meta:
        verbose_name = 'pessoa'
        verbose_name_plural = 'pessoas'

    nome = models.CharField(max_length=50, verbose_name='nome')
    sobrenome = models.CharField(max_length=100, verbose_name='sobrenome')
    email = models.EmailField(verbose_name='e-mail')


class Professor(Pessoa):
    class Meta:
        verbose_name = 'professor'
        verbose_name_plural = 'professores'

    def __str__(self):
        return '[Professor] ' + self.nome + ' ' + self.sobrenome

    universidade = models.CharField(max_length=100, verbose_name='universidade')


class Materia(models.Model):
    class Meta:
        verbose_name = 'matéria'
        verbose_name_plural = 'matérias'

    def __str__(self):
        return self.nomeDisciplina + ' (' + str(self.ano) + '/' + str(self.semestre) + ')'

    ano = models.IntegerField(verbose_name='ano')
    semestre = models.IntegerField(verbose_name='semestre')
    turma = models.CharField(max_length=1, verbose_name='turma')
    nomeDisciplina = models.CharField(max_length=200, verbose_name='nome da disciplina')
    codigoInscricao = models.CharField(max_length=30, verbose_name='código de inscrição', unique=True)
    professor = models.ForeignKey(Professor, verbose_name='professor(a)')
    perguntas = models.ManyToManyField(Pergunta, verbose_name='perguntas', blank=True)
    materiaAtiva = models.BooleanField(verbose_name='matéria ativa?', default=True)


class Resposta(models.Model):
    class Meta:
        verbose_name = 'resposta'
        verbose_name_plural = 'respostas'

    def __str__(self):
        return ""

    materia = models.ForeignKey(Materia, verbose_name='matéria')


class Aluno(Pessoa):
    class Meta:
        verbose_name = 'aluno'
        verbose_name_plural = 'alunos'

    def __str__(self):
        return '[Aluno] ' + self.nome + ' ' + self.sobrenome

    curso = models.CharField(max_length=100, verbose_name='curso')
    materias = models.ManyToManyField(Materia, verbose_name='matérias inscritas', blank=True)
    perguntas_respondidas = models.ManyToManyField(Resposta, verbose_name='perguntas respondidas', blank=True)
