from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from pyqrcode import QRCode
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings
import base64
import requests


def index(request):
    return HttpResponse("Home")

OK = 'ok'
ERRO = 'error'
STATUS = 'status'
DESCRICAO = 'descricao'
REQUISICAO_GET = 'Requisição GET ao invés de requisição POST.'
REQUISICAO_OK = {'status': 'ok'}
ERRO_PARAMETROS_INVALIDOS = 'Erro na requisição. Parâmetros inválidos.'


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
        'curso': aluno.curso.nome_curso,
        'foto': aluno.foto_url
    }


def dicionario_alunos(alunos, materia):
    return {
        STATUS: OK,
        'materia': materia.id,
        'alunos': [dicionario_aluno(aluno) for aluno in alunos]
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
        'nome_materia': materia.nome_materia,
        'codigo_inscricao': materia.codigo_inscricao,
        'professor': dicionario_professor(materia.professor)
    }


def dicionario_materias_com_perguntas_sem_professor(materia, perguntas):
    materia_sem_professor = {
        'codigo': materia.id,
        'ano': materia.ano,
        'semestre': materia.semestre,
        'turma': materia.turma,
        'nome_materia': materia.nome_materia,
        'codigo_inscricao': materia.codigo_inscricao,
        'perguntas': perguntas
    }

    dict = {}

    for i in [materia_sem_professor, perguntas]:
        dict.update(i)

    return dict


def dicionario_materias(materias):
    return {
        STATUS: OK,
        'materias': materias
    }


def dicionario_alternativa(alternativa):
    return {
        'codigo': alternativa.id,
        'letra': alternativa.letra,
        'texto_alternativa': alternativa.texto_alternativa,
    }

def dicionario_alternativas(alternativas):
    return {
        STATUS: OK,
        'alternativas': [dicionario_alternativa(alternativa) for alternativa in alternativas],
        'alternativas_corretas': [alternativa.letra for alternativa in alternativas.filter(is_correta=True)]
    }


def dicionario_pergunta(pergunta):
    return {
        'codigo': pergunta.id,
        'titulo': pergunta.titulo,
        'texto_pergunta': pergunta.texto_pergunta,
        'alternativas': [dicionario_alternativa(alternativa) for alternativa in pergunta.alternativas.all().order_by('letra')],
        'alternativas_corretas': [alternativa.letra for alternativa in pergunta.alternativas.filter(is_correta=True).order_by('letra')],
        'data_aproximada': pergunta.data_aproximada
    }


def dicionario_perguntas(perguntas):
    return {
        STATUS: OK,
        'perguntas': [dicionario_pergunta(pergunta) for pergunta in perguntas]
    }


@csrf_exempt
def getAluno(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            # TODO: adicionar status OK no dicionário
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
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            professor = Professor.objects.get(email=email)
            return JsonResponse(dicionario_professor(professor))
        except:
            return JsonResponse(erro("Professor não encontrado com o e-mail cadastrado."))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarAluno(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            curso = request.POST['curso']
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))

        try:
            aluno_ja_existente = True if len(Aluno.objects.filter(email=email)) > 0 else False

            if aluno_ja_existente:
                return JsonResponse(erro('Aluno com e-mail ' + email + 'já cadastrado.'))
            else:
                curso = Curso(nome_curso=curso)
                aluno = Aluno(nome=nome, sobrenome=sobrenome, email=email, curso=curso)
                aluno.save()
                return JsonResponse(dicionario_aluno(aluno))
        except:
            return JsonResponse(erro('Erro ao cadastrar aluno.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarProfessor(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            universidade = request.POST['universidade']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            professor_ja_existente = True if len(Professor.objects.filter(email=email)) > 0 else False

            if professor_ja_existente:
                return JsonResponse(erro('Professor com e-mail ' + email + 'já cadastrado.'))
            else:
                professor = Professor(nome=nome, sobrenome=sobrenome, email=email, universidade=universidade)
                professor.save()
                return JsonResponse(dicionario_professor(professor))
        except:
            return JsonResponse(erro('Erro ao cadastrar professor.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getMaterias(request):
    if request.method == 'POST':
        try:
            status_materia = request.POST['status_materia']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            if status_materia == 'inativa':
                return getMateriasPorStatus(request, status_materia=False)
            else:
                return getMateriasPorStatus(request, status_materia=True)
        except:
            return JsonResponse(erro('Erro ao obter a lista de matérias.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getAlunosInscritosPorMateria(request):
    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            materia = Materia.objects.get(id=codigo_materia)
            alunos_inscritos = Materia.objects.get(id=codigo_materia).aluno_set.all().order_by('nome', 'sobrenome')

            alunos = []

            for aluno in alunos_inscritos:
                alunos.append(dicionario_aluno(aluno))

            # TODO: Corrigir a chamada para dicionario_alunos
            return JsonResponse(dicionario_alunos(alunos, materia))
        except:
            return JsonResponse(erro('Erro ao obter lista de alunos inscritos nesta disciplina.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getMateriasPorStatus(request, status_materia):
    if request.method == 'POST':
        # TODO: Melhorar a identificação de perfil do usuário
        try:
            email = request.POST['email']
            tipo_usuario = request.POST['tipo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            materias = []

            if tipo_usuario == 'aluno':
                aluno = Aluno.objects.get(email=email)
                materias_encontradas = aluno.materias.filter(materiaAtiva=status_materia). \
                    order_by('-ano', '-semestre', 'nome_materia')
            else:
                professor = Professor.objects.get(email=email)
                materias_encontradas = Materia.objects.filter(professor=professor).filter(materiaAtiva=status_materia). \
                    order_by('-ano', '-semestre', 'nome_materia')

            for materia in materias_encontradas:
                materias.append(dicionario_materia(materia))

            return JsonResponse(dicionario_materias(materias))
        except:
            return JsonResponse(erro('Erro ao obter lista de matérias.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))

# TODO: Continuar revisão a partir daqui
@csrf_exempt
def getMateriaPorQRCode(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo']
            email_aluno = request.POST['email']
            try:
                aluno = Aluno.objects.get(email=email_aluno)

                try:
                    inscricao_ja_existente = aluno.materias.get(codigo_inscricao=codigo)
                    inscricao_ja_existente = True
                except:
                    inscricao_ja_existente = False

                if inscricao_ja_existente:
                    return JsonResponse(erro('Aluno já inscrito nesta matéria.'))
                else:
                    try:
                        materia = Materia.objects.get(codigo_inscricao=codigo)

                        if materia.materiaAtiva:
                            return JsonResponse(dicionario_materia(materia))
                        else:
                            return JsonResponse(erro('Esta matéria está atualmente inativa.'))
                    except:
                        return JsonResponse(erro('O código deste QR não foi encontrado no cadastro de matérias.'))
            except:
                return JsonResponse(erro('Aluno não cadastrado.'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def cadastrarMateria(request):
    if request.method == 'POST':
        try:
            ano = request.POST['ano']
            semestre = request.POST['semestre']
            turma = request.POST['turma']
            nome_disciplina = request.POST['nome_materia']
            codigo_inscricao = request.POST['codigo_inscricao']
            emailProfessor = request.POST['email']

            try:
                professor = Professor.objects.get(email=emailProfessor)
                try:
                    nova_materia = Materia(ano=ano, semestre=semestre, turma=turma, nome_materia=nome_disciplina,
                                           codigo_inscricao=codigo_inscricao, professor=professor)
                    nova_materia.save()
                    return JsonResponse(dicionario_materia(nova_materia))
                except:
                    return JsonResponse(erro('Código de inscrição já cadastrado para outra matéria.'))
            except:
                return JsonResponse(erro('Professor não cadastrado.'))
        except:
            return JsonResponse(erro('Parâmetros inválidos.'))
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
            materia = Materia.objects.get(codigo_inscricao=codigo_inscricao)

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
            data_aproximada = request.POST['data_aproximada']

            dia = int(data_aproximada[0:2])
            mes = int(data_aproximada[3:5])
            ano = int(data_aproximada[6:])

            data_aproximada = datetime.date(ano, mes, dia)

            try:
                professor = Professor.objects.get(email=email_professor)

                pergunta = Pergunta(titulo=titulo, texto_pergunta=texto_pergunta, disponivel=False, data_aproximada=data_aproximada)
                pergunta.save()

                try:
                    for i in range(0, quantidade_alternativas):
                        letra_alternativa = request.POST['alternativa' + str(i) + '_letra']
                        texto_alternativa = request.POST['alternativa' + str(i) + '_texto_alternativa']
                        alternativa_correta = True if request.POST['alternativa' + str(i) + '_correta'] == 'true' else False

                        alternativa = Alternativa(letra=letra_alternativa, texto_alternativa=texto_alternativa,
                                                  is_correta=alternativa_correta)
                        alternativa.save()
                        pergunta.alternativas.add(alternativa)
                        pergunta.save()

                    professor.materia_set.get(id=codigo_materia).perguntas.add(pergunta)
                    professor.save()

                    return JsonResponse(REQUISICAO_OK)
                except:
                    return JsonResponse(erro('Erro na requisição. Parâmetros das alternativas inválidos.'))
            except:
                return JsonResponse(erro('Erro na requisição. Professor(a) não encontrado(a).'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getPerguntasPorMateria(request):
    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']

            try:
                materia = Materia.objects.get(id=codigo_materia)
                perguntas = materia.perguntas.all().order_by('data_aproximada')

                return JsonResponse(dicionario_perguntas(perguntas))
            except:
                return JsonResponse(erro('Erro na requisição. Código de matéria inválido.'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getPerguntasPorProfessor(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']

            try:
                professor = Professor.objects.get(email=email)

                materias = Materia.objects.filter(professor=professor).filter(materiaAtiva=True).\
                    order_by('-ano', '-semestre', 'nome_materia')

                materias_perguntas = []

                for materia in materias:
                    materias_perguntas.append(dicionario_materias_com_perguntas_sem_professor(materia,
                                                                                              dicionario_perguntas(materia.perguntas.all().order_by('data_aproximada'))))

                return JsonResponse({
                    STATUS: OK,
                    'materias': materias_perguntas
                })

            except:
                return JsonResponse(erro('Erro na requisição. Professor não encontrado.'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getAlternativasPorPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']

            pergunta = Pergunta.objects.get(id=codigo_pergunta)

            alternativas = pergunta.alternativas.all().order_by('letra')

            return JsonResponse(dicionario_alternativas(alternativas))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getRespostasPorPerguntaPorAluno(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            aluno = Aluno.objects.get(email=email)
            perguntas_respondidas = []

            for pergunta_respondida in aluno.perguntas_respondidas.all():
                perguntas_respondidas.append({
                    'pergunta': pergunta_respondida.pergunta.id,
                    'respostas': [alternativa.letra for alternativa in pergunta_respondida.respostas.all()]
                })

            return JsonResponse({
                STATUS: OK,
                'perguntas_respondidas': perguntas_respondidas
            })

        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getQuantidadeDeRespostasPorAlternativaPorPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']

            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            quantidade_respostas = []

            for alternativa in pergunta.alternativas.all().order_by('letra'):

                q = PerguntaRespondida.objects.filter(respostas=alternativa).count()
                quantidade_respostas.append({'alternativa': alternativa.letra, 'quantidade_respostas': q})

            return JsonResponse({
                STATUS: OK,
                'pergunta': pergunta.id,
                'quantidade_respostas': quantidade_respostas
            })
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getQuantidadeDeRespostasTotaisPorPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']

            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            quantidade_respostas = 0

            # TODO: contar quantas pessoas responderam, não quantas alternativas
            for alternativa in pergunta.alternativas.all():
                quantidade_respostas += PerguntaRespondida.objects.filter(respostas=alternativa).count()

            return JsonResponse({
                STATUS: OK,
                'pergunta': pergunta.id,
                'quantidade_respostas_total': quantidade_respostas
            })
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def enviarQRCodePorEmail(request):

    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']
            email_professor = request.POST['email']

            try:

                professor = Professor.objects.get(email=email_professor)
                materia = Materia.objects.get(id=codigo_materia)

                try:
                    qr_code = QRCode(materia.codigo_inscricao)
                    qr_code.png(file=settings.BASE_DIR + '/pergunte/static/pergunte/code.png', scale=5)

                    try:
                        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

                        from_email = Email(professor.nome + ' ' + professor.sobrenome + '<' + professor.email + '>')
                        subject = 'QRCode da matéria "' + materia.nome_materia + '"'

                        conteudo_do_email = """
                        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                        <html>
                        <head>
                            <meta charset="utf-8"/>
                            <title>QR Code da matéria #NOMEMATERIA</title>
                        </head>
                        <body>
                            <h1>QR Code da matéria "#NOMEMATERIA"</h1>
                            <p>Olá professor(a) #NOME!</p>
                            <p>Segue em anexo o QR code com o código <b>#CODIGO</b> referente à matéria <b>#NOMEMATERIA</b>,
                            como solicitado pelo app Pergunte.</p>
                        </body>
                        </html>
                        """

                        conteudo_do_email = conteudo_do_email.replace('#NOMEMATERIA', materia.nome_materia)
                        conteudo_do_email = conteudo_do_email.replace('#NOME', professor.nome)
                        conteudo_do_email = conteudo_do_email.replace('#CODIGO', materia.codigo_inscricao)

                        content = Content('text/html', conteudo_do_email)

                        ready_mail = Mail(from_email, subject, from_email, content)

                        anexo = Attachment()

                        with open(settings.BASE_DIR + '/pergunte/static/pergunte/code.png', 'rb') as f:
                            data = f.read()
                            f.close()

                        encoded = base64.b64encode(data).decode('UTF-8')

                        anexo.set_content(encoded)
                        anexo.set_type("image/png")
                        anexo.set_filename('code.png')
                        anexo.set_disposition("inline")
                        anexo.set_content_id("QRCode")
                        ready_mail.add_attachment(anexo)

                        response = sg.client.mail.send.post(request_body=ready_mail.get())

                        if response.status_code >= 200 and response.status_code < 300:
                            return JsonResponse({
                                STATUS: OK
                            })
                        else:
                            return JsonResponse(erro('Erro de conexão com a API de envio de e-mail.'))
                    except:
                        return JsonResponse(erro('Erro no envio do e-mail.'))
                except:
                    return JsonResponse(erro('Erro na geração do QR code.'))
            except:
                return JsonResponse(erro('Erro na requisição. Professor ou matéria inválidos.'))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getAlunosInscritosPorMateria(request):
    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']
            materia = Materia.objects.get(id=codigo_materia)
            alunos = Aluno.objects.filter(materias=materia).order_by('nome', 'sobrenome')

            return JsonResponse(dicionario_alunos(alunos, materia))
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getPerguntasAtivasPorMateria(request):
    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            materia = Materia.objects.get(id=codigo_materia)
            perguntas = materia.perguntas.filter(disponivel=True)

            # TODO: remover as perguntas já respondidas do retorno

            return JsonResponse(dicionario_perguntas(perguntas))
        except:
            return JsonResponse(erro('Erro na requisição. Matéria não encontrada.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getProximasPerguntasPorMateria(request):
    if request.method == 'POST':
        try:
            data = request.POST['data']
            codigo_materia = request.POST['codigo']

        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            dia = int(data[0:2])
            mes = int(data[3:5])
            ano = int(data[6:])

            data = datetime.date(ano, mes, dia)

            materia = Materia.objects.get(id=codigo_materia)

            perguntas = []
            # TODO: remover as perguntas já respondidas da lista de retorno
            for pergunta in materia.perguntas.filter(data_aproximada__gte=data).order_by('data_aproximada', 'titulo'):
                perguntas.append(pergunta)

            return JsonResponse(dicionario_perguntas(perguntas))

        except:
            return JsonResponse(erro('Erro na requisição.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getPerguntasRespondidasPorMateria(request):
    if request.method == 'POST':
        try:
            codigo_materia = request.POST['codigo']
            email_usuario = request.POST['email']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            aluno = Aluno.objects.get(email=email_usuario)
            materia = Materia.objects.get(id=codigo_materia)

            perguntas_respondidas = PerguntaRespondida.objects.filter(aluno=aluno).filter(pergunta__materia=materia).\
                order_by('-pergunta__data_aproximada', 'pergunta__titulo')

            perguntas_respondidas = [Pergunta.objects.get(id=p.pergunta_id) for p in perguntas_respondidas]

            return JsonResponse(dicionario_perguntas(perguntas_respondidas))

        except:
            return JsonResponse(erro('Erro na requisição'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def disponibilizarPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            pergunta.disponivel = True
            pergunta.save()

            return JsonResponse(REQUISICAO_OK)
        except:
            return JsonResponse('Erro na requisição. Pergunta não encontrada.')
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def finalizarPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            pergunta.disponivel = False
            pergunta.save()

            return JsonResponse(REQUISICAO_OK)
        except:
            return JsonResponse('Erro na requisição. Pergunta não encontrada.')
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def registrarReposta(request):
    if request.method == 'POST':
        try:
            email_aluno = request.POST['email']
            codigo_pergunta = request.POST['codigo']
            quantidade_alternativas = int(request.POST['quantidade_alternativas'])
            alternativas = []

            for i in range(0, quantidade_alternativas):
                alternativas.append(request.POST['alternativa' + str(i) + '_codigo'])

        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))

        try:
            pergunta = Pergunta.objects.get(id=codigo_pergunta)

            if not pergunta.disponivel:
                return JsonResponse(erro('Erro ao registrar a resposta. Esta pergunta já não está mais disponível.'))
            else:
                aluno = Aluno.objects.get(email=email_aluno)
                pergunta_respondida = PerguntaRespondida(pergunta=pergunta, data_hora_resposta=datetime.datetime.now())
                pergunta_respondida.save()

                for i in range(0, quantidade_alternativas):
                    alternativa = Alternativa.objects.get(id=alternativas[i])
                    pergunta_respondida.respostas.add(alternativa)

                pergunta_respondida.save()
                aluno.perguntas_respondidas.add(pergunta_respondida)
                aluno.save()

                return JsonResponse(REQUISICAO_OK)

        except:
            return JsonResponse(erro('Erro na requisição. Resposta não registrada.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getRespostasPorPergunta(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))

        try:
            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            quantidade_alternativas = pergunta.alternativas.count()

            quantidades_respostas = {}
            if quantidade_alternativas == 1:
                quantidades_respostas = {STATUS: OK, 'quantidade_alternativas': quantidade_alternativas, 'pergunta': codigo_pergunta, 'A': 0}
            elif quantidade_alternativas == 2:
                quantidades_respostas = {STATUS: OK, 'quantidade_alternativas': quantidade_alternativas, 'pergunta': codigo_pergunta, 'A': 0, 'B': 0}
            elif quantidade_alternativas == 3:
                quantidades_respostas = {STATUS: OK, 'quantidade_alternativas': quantidade_alternativas, 'pergunta': codigo_pergunta, 'A': 0, 'B': 0, 'C': 0}
            elif quantidade_alternativas == 4:
                quantidades_respostas = {STATUS: OK, 'quantidade_alternativas': quantidade_alternativas, 'pergunta': codigo_pergunta, 'A': 0, 'B': 0, 'C': 0, 'D': 0}
            elif quantidade_alternativas == 5:
                quantidades_respostas = {STATUS: OK, 'quantidade_alternativas': quantidade_alternativas, 'pergunta': codigo_pergunta, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

            respostas = PerguntaRespondida.objects.filter(pergunta=pergunta)

            for resposta in respostas:
                for alternativa in resposta.respostas.all():
                    quantidades_respostas[alternativa.letra] += 1

            return JsonResponse(quantidades_respostas)

        except:
            return JsonResponse(erro('Erro na requisição. Pergunta não encontrada.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def getEstatisticas(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
        except:
            return JsonResponse(erro('Erro na requisição. Parâmetros inválidos.'))

        try:
            aluno = Aluno.objects.get(email=email)
            perguntas_respondidas = PerguntaRespondida.objects.filter(aluno=aluno)

            quantidade_perguntas_respondidas = len(perguntas_respondidas)

            respondidas_corretamente = 0

            for p in perguntas_respondidas:
                respostas_do_aluno = p.respostas.all()
                corretas_da_pergunta = p.pergunta.alternativas.filter(is_correta=True)

                acertou = True
                for r in respostas_do_aluno:
                    if r not in corretas_da_pergunta:
                        acertou = False

                if acertou:
                    respondidas_corretamente += 1

            quantidade_materias_inscritas = aluno.materias.count()

            return JsonResponse({
                STATUS: OK,
                'quantidade_perguntas_respondidas': quantidade_perguntas_respondidas,
                'quantidade_materias_inscritas': quantidade_materias_inscritas,
                'quantidade_perguntas_respondidas_corretamente': respondidas_corretamente
            })

        except:
            return JsonResponse(erro('Erro na requisição. Aluno não encontrado.'))

    else:
        return JsonResponse(erro(REQUISICAO_GET))


@csrf_exempt
def enviarNotificacao(request):
    if request.method == 'POST':
        try:
            codigo_pergunta = request.POST['codigo']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            pergunta = Pergunta.objects.get(id=codigo_pergunta)
            materia = Materia.objects.get(perguntas=pergunta)
            alunos_inscritos = materia.aluno_set.all().order_by('nome', 'sobrenome')

            url = 'https://fcm.googleapis.com/fcm/send'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': settings.FIREBASE_CLOUD_MESSAGING_KEY
            }

            status = 'nenhum'
            for aluno in alunos_inscritos:
                notificacao = {
                    'to': aluno.firebase_token,
                    'notification': {
                        'title': 'Pergunte: nova pergunta ativa',
                        'body': 'Uma nova pergunta está disponível para ser respondida na matéria ' +
                                materia.nome_materia + '.'
                    }
                }
                status = requests.post(url, headers=headers, json=notificacao)

            return JsonResponse({STATUS: OK, 'quant': status})
        except:
            return JsonResponse(erro('Erro ao obter lista de alunos inscritos nesta disciplina.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))


def setarTokenEFoto(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            token = request.POST['token']
            foto_url = request.POST['foto']
        except:
            return JsonResponse(erro(ERRO_PARAMETROS_INVALIDOS))

        try:
            p = Pessoa.objects.get(email=email)
            p.firebase_token = token
            p.foto_url = foto_url
            p.save()

            return JsonResponse({STATUS: OK})
        except:
            return JsonResponse(erro('Erro na requisição. Usuário não encontrado.'))
    else:
        return JsonResponse(erro(REQUISICAO_GET))
