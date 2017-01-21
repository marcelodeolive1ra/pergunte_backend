from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Home")

OK = 'ok'
ERRO = 'error'
STATUS = 'status'
DESCRICAO = 'descricao'
REQUISICAO_GET = 'Requisição GET ao invés de requisição POST.'
REQUISICAO_OK = {'status': 'ok'}

def erro(mensagemDeErro):
    return {
        STATUS: ERRO,
        DESCRICAO: mensagemDeErro
    }

def dicionario_aluno(aluno):
    return {
        STATUS: OK,
        'nome': aluno.nome,
        'sobrenome': aluno.sobrenome,
        'email': aluno.email,
        'curso': aluno.curso
    }


def dicionario_alunos(alunos):
    return {
        STATUS: OK,
        'alunos': alunos
    }

def dicionario_professor(professor):
    return {
        STATUS: OK,
        'nome': professor.nome,
        'sobrenome': professor.sobrenome,
        'email': professor.email,
        'universidade': professor.universidade
    }


def dicionario_materia(materia):
    return {
        STATUS: OK,
        'codigo': materia.id,
        'ano': materia.ano,
        'semestre': materia.semestre,
        'turma': materia.turma,
        'nome_materia': materia.nomeDisciplina,
        'codigo_inscricao': materia.codigoInscricao,
        'professor': {
            'nome': materia.professor.nome,
            'sobrenome': materia.professor.sobrenome,
            'email': materia.professor.email,
            'universidade': materia.professor.universidade
        }
    }


def dicionario_materias(materias):
    return {
        STATUS: OK,
        'materias': materias
    }




@csrf_exempt
def getAluno(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            aluno = Aluno.objects.get(email=email)
            return JsonResponse(dicionario_aluno(aluno))
        except:
            return JsonResponse(erro("Não foi encontrado aluno com o e-mail informado."))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getProfessor(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            professor = Professor.objects.get(email=email)
            return JsonResponse(dicionario_professor(professor))
        except:
            return JsonResponse(erro("Não foi encontrado professor com o e-mail informado."))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarAluno(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']

            alunoJaExistente = True if len(Aluno.objects.filter(email=email)) > 0 else False

            if alunoJaExistente:
                return JsonResponse(erro('Aluno com e-mail ' + email + 'já cadastrado.'))
            else:
                nome = request.POST['nome']
                sobrenome = request.POST['sobrenome']
                curso = request.POST['curso']
                aluno = Aluno(nome=nome, sobrenome=sobrenome, email=email, curso=curso)
                aluno.save()
                return JsonResponse(dicionario_aluno(aluno))
        except:
            return JsonResponse(erro('Não foi possível cadastrar o aluno.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarProfessor(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']

            professorJaExistente = True if len(Professor.objects.filter(email=email)) > 0 else False

            if professorJaExistente:
                return JsonResponse(erro('Professor com e-mail ' + email + 'já cadastrado.'))
            else:
                nome = request.POST['nome']
                sobrenome = request.POST['sobrenome']
                universidade = request.POST['universidade']
                professor = Professor(nome=nome, sobrenome=sobrenome, email=email, universidade=universidade)
                professor.save()
                return JsonResponse(dicionario_professor(professor))
        except:
            return JsonResponse(erro('Não foi possível cadastrar o professor.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getMaterias(request):
    if request.method == 'POST':
        try:
            statusMateria = request.POST['status_materia']

            if statusMateria == 'inativa':
                return getMateriasPorStatus(request, statusMateria=False)
            else:
                return getMateriasPorStatus(request, statusMateria=True)
        except:
            return JsonResponse(erro('Erro ao obter a lista de matérias.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getAlunosInscritosPorMateria(request):
    if request.method == 'POST':
        try:
            codigoMateria = request.POST['codigo']

            alunosInscritos = Materia.objects.get(id=codigoMateria).aluno_set.all().order_by('nome', 'sobrenome')

            alunos = []

            for aluno in alunosInscritos:
                alunos.append(dicionario_aluno(aluno))

            return JsonResponse(dicionario_alunos(alunos))
        except:
            return JsonResponse(erro('Erro ao obter lista de alunos inscritos nesta disciplina.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getMateriasPorStatus(request, statusMateria):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            tipoUsuario = request.POST['tipo']

            materias = []

            if tipoUsuario == 'aluno':
                aluno = Aluno.objects.get(email=email)
                materias_encontradas = aluno.materias.filter(materiaAtiva=statusMateria). \
                    order_by('-ano', '-semestre', 'nomeDisciplina')
            else:
                professor = Professor.objects.get(email=email)
                materias_encontradas = Materia.objects.filter(professor=professor).filter(materiaAtiva=statusMateria). \
                    order_by('-ano', '-semestre', 'nomeDisciplina')

            for materia in materias_encontradas:
                materias.append(dicionario_materia(materia))

            return JsonResponse(dicionario_materias(materias))
        except:
            return JsonResponse(erro('Erro ao obter lista de matérias.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getMateriaPorQRCode(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo']
            email_aluno = request.POST['email']
            aluno = Aluno.objects.get(email=email_aluno)
            inscricaoJaExistente = True if len(aluno.materias.filter(codigoInscricao=codigo)) > 0 else False

            if inscricaoJaExistente:
                return JsonResponse(erro('Aluno já inscrito nesta matéria.'))
            else:
                materia = Materia.objects.filter(codigoInscricao=codigo)

                materiaExistente = True if len(materia) > 0 else False

                if materiaExistente:
                    materia = materia[0]

                    if materia.materiaAtiva:
                        return JsonResponse(dicionario_materia(materia))
                    else:
                        return JsonResponse(erro('Esta matéria está atualmente inativa.'))
                else:
                    return JsonResponse(erro('O código deste QR não foi encontrado no cadastro de matérias.'))
        except:
            return JsonResponse(erro('Erro na requisição.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarMateria(request):
    if request.method == 'POST':
        try:
            ano = request.POST['ano']
            semestre = request.POST['semestre']
            turma = request.POST['turma']
            nomeDisciplina = request.POST['nome_materia']
            codigoInscricao = request.POST['codigo_inscricao']
            emailProfessor = request.POST['email']

            try:
                professor = Professor.objects.get(email=emailProfessor)
                nova_materia = Materia(ano=ano, semestre=semestre, turma=turma, nomeDisciplina=nomeDisciplina,
                                       codigoInscricao=codigoInscricao, professor=professor)
                nova_materia.save()
                return JsonResponse(dicionario_materia(nova_materia))
            except:
                return JsonResponse(erro('Professor não cadastrado.'))
        except:
            return JsonResponse(erro('Erro na requisição.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cancelarInscricaoEmMateria(request):
    if request.method == 'POST':
        try:
            email_aluno = request.POST['email']
            codigo_materia = request.POST['codigo']
            aluno = Aluno.objects.get(email=email_aluno)
            materia = Materia.objects.get(id=codigo_materia)
            aluno.materias.remove(materia)
            aluno.save()
            return JsonResponse(dicionario_materia(materia))
        except:
            return JsonResponse(erro('Erro na requisição. Aluno ou matéria não encontrados.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def inscreverAlunoEmMateria(request):
    if request.method == 'POST':
        try:
            email_aluno = request.POST['email']
            codigo_inscricao = request.POST['codigo']
            aluno = Aluno.objects.get(email=email_aluno)
            materia = Materia.objects.get(codigoInscricao=codigo_inscricao)

            if materia.materiaAtiva:
                aluno.materias.add(materia)
                aluno.save()
                return JsonResponse(dicionario_materia(materia))
            else:
                return JsonResponse(erro('Não é possível cadastrá-lo nesta matéria, pois ela está inativa.'))

            # TODO Tratar erro de quando a matéria já está cadastrada para este usuário
            # Fazer por segurança, embora método getMateriaPorQRCode já faz essa verificação

        except:
            return JsonResponse(erro('Erro na requisição. Aluno ou matéria não encontrados.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))

@csrf_exempt
def buscarPerfilUsuario(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            aluno = Aluno.objects.get(email=email)
            return JsonResponse(dicionario_aluno(aluno))
        except:
            try:
                professor = Professor.objects.get(email=email)
                return JsonResponse(dicionario_professor(professor))
            except:
                return JsonResponse(erro('Perfil não encontrado'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def desativarMateria(request):
    if request.method == 'POST':
        try:
            email_professor = request.POST['email']
            codigo_materia = request.POST['codigo']
            professor = Professor.objects.get(email=email_professor)
            materia = Materia.objects.get(id=codigo_materia)
            materia.materiaAtiva = False
            materia.save()

            return JsonResponse(dicionario_materia(materia))
        except:
            return JsonResponse(erro('Erro ao desativar matéria.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarPergunta(request):
    if request.method == 'POST':
        try:
            email_professor = request.POST['email']
            titulo = request.POST['titulo']
            texto_pergunta = request.POST['texto_pergunta']
            codigo_materia = request.POST['codigo']
            quantidade_alternativas = int(request.POST['quantidade_alternativas'])

            try:
                professor = Professor.objects.get(email=email_professor)

                pergunta = Pergunta(titulo=titulo, texto_pergunta=texto_pergunta, disponivel=False)
                pergunta.save()

                try:
                    for i in range(0, quantidade_alternativas):
                        letra_alternativa = request.POST['alternativa' + str(i) + '_letra']
                        texto_alternativa = request.POST['alternativa' + str(i) + '_texto_alternativa']
                        alternativa_correta = True if request.POST['alternativa' + str(i) + '_correta'] == 'true' else False

                        alternativa = Alternativa(letra=letra_alternativa, textoAlternativa=texto_alternativa, alternativaCorreta=alternativa_correta)
                        alternativa.save()
                        pergunta.alternativas.add(alternativa)
                        pergunta.save()

                    professor.materia_set.get(id=codigo_materia).perguntas.add(pergunta)
                    professor.save()
                except:
                    return JsonResponse(erro('Erro na requisição. Parâmetros das alternativas inválidos.'))
                return JsonResponse({'status': 'ok'})
            except:
                return JsonResponse(erro('Erro na requisição. Professor(a) não encontrado(a).'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))

