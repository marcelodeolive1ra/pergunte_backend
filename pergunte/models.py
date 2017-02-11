from django.db import models


class Alternativa(models.Model):
    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __str__(self):
        return '[Alternativa ' + self.letra + '] ' + self.texto_alternativa

    letra = models.CharField(max_length=1, verbose_name='alternativa')
    texto_alternativa = models.TextField(verbose_name='texto da alternativa', blank=True)
    is_correta = models.BooleanField(verbose_name='alternativa correta?', default=False)


class Pergunta(models.Model):
    class Meta:
        verbose_name = 'pergunta'
        verbose_name_plural = 'perguntas'

    def __str__(self):
        return '[Pergunta] ' + self.titulo

    titulo = models.CharField(max_length=50, verbose_name='titulo/tag', blank=True)
    texto_pergunta = models.TextField(verbose_name='texto da pergunta', blank=True)
    alternativas = models.ManyToManyField(Alternativa, verbose_name='alternativas', blank=True)
    disponivel = models.BooleanField(verbose_name='pergunta disponível?')
    data_aproximada = models.DateField(blank=True)


class Pessoa(models.Model):
    class Meta:
        verbose_name = 'pessoa'
        verbose_name_plural = 'pessoas'

    nome = models.CharField(max_length=50, verbose_name='nome')
    sobrenome = models.CharField(max_length=100, verbose_name='sobrenome')
    email = models.EmailField(verbose_name='e-mail')
    firebase_user_id = models.CharField(max_length=100, verbose_name='Firebase ID', null=True) # null temporariamente


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
        return self.nome_materia + ' (' + str(self.ano) + '/' + str(self.semestre) + ')'

    ano = models.IntegerField(verbose_name='ano')
    semestre = models.IntegerField(verbose_name='semestre')
    turma = models.CharField(max_length=1, verbose_name='turma')
    nome_materia = models.CharField(max_length=200, verbose_name='nome da matéria')
    codigo_inscricao = models.CharField(max_length=30, verbose_name='código de inscrição', unique=True)
    professor = models.ForeignKey(Professor, verbose_name='professor(a)')
    perguntas = models.ManyToManyField(Pergunta, verbose_name='perguntas', blank=True)
    materiaAtiva = models.BooleanField(verbose_name='matéria ativa?', default=True)


class PerguntaRespondida(models.Model):
    class Meta:
        verbose_name = 'pergunta respondida'
        verbose_name_plural = 'perguntas respondidas'

    def __str__(self):
        return 'Pergunta respondida'

    pergunta = models.ForeignKey(Pergunta, verbose_name='pergunta')
    respostas = models.ManyToManyField(Alternativa, verbose_name='respostas', blank=True)
    data_hora_resposta = models.DateTimeField(verbose_name='data/hora da resposta')


class Curso(models.Model):
    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

    def __str__(self):
        return self.nome_curso

    nome_curso = models.CharField(max_length=100, verbose_name='curso')


class Aluno(Pessoa):
    class Meta:
        verbose_name = 'aluno'
        verbose_name_plural = 'alunos'

    def __str__(self):
        return '[Aluno] ' + self.nome + ' ' + self.sobrenome

    curso = models.ForeignKey(Curso, verbose_name='curso')
    materias = models.ManyToManyField(Materia, verbose_name='matérias inscritas', blank=True)
    perguntas_respondidas = models.ManyToManyField(PerguntaRespondida, verbose_name='perguntas respondidas', blank=True)
