from .models import Professor, Aluno, Materia
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Home")

@csrf_exempt
def getAluno(request):
    if request.method == 'POST':
        email = request.POST['email']
        aluno = Aluno.objects.filter(email=email)

        encontrado = True if len(aluno) > 0 else False

        if encontrado:
            aluno = aluno[0]
            return JsonResponse({'status': 'ok',
                                 'nome': aluno.nome,
                                 'sobrenome': aluno.sobrenome,
                                 'curso': aluno.curso})
        else:
            return JsonResponse({'status': 'error',
                                 'descricao': 'Aluno não encontrado.'})
    else:
        return JsonResponse({'status': 'error',
                             'descricao': 'Requisição sem e-mail.'})


@csrf_exempt
def getProfessor(request):
    if request.method == 'POST':
        email = request.POST['email']
        professor = Professor.objects.filter(email=email)

        encontrado = True if len(professor) > 0 else False

        if encontrado:
            professor = professor[0]
            return JsonResponse({'status': 'ok',
                                 'nome': professor.nome,
                                 'sobrenome': professor.sobrenome,
                                 'curso': professor.universidade})
        else:
            return JsonResponse({'status': 'error',
                                 'descricao': 'Professor não encontrado.'})
    else:
        return JsonResponse({'status': 'error',
                             'descricao': 'Requisição sem e-mail.'})


@csrf_exempt
def cadastrarAluno(request):
    if request.method == 'POST':
        email = request.POST['email']

        alunoJaExistente = True if len(Aluno.objects.filter(email=email)) > 0 else False

        if alunoJaExistente:
            return JsonResponse({'status': 'error',
                                 'descricao': 'Aluno já cadastrado'})
        else:
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            curso = request.POST['curso']
            aluno = Aluno(nome=nome, sobrenome=sobrenome, email=email, curso=curso)
            aluno.save()
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def cadastrarProfessor(request):
    if request.method == 'POST':
        email = request.POST['email']

        professorJaExistente = True if len(Professor.objects.filter(email=email)) > 0 else False

        if professorJaExistente:
            return JsonResponse({'status': 'error', 'descricao': 'Professor já cadastrado'})
        else:
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            universidade = request.POST['universidade']
            aluno = Professor(nome=nome, sobrenome=sobrenome, email=email, universidade=universidade)
            aluno.save()
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error',
                             'descricao': 'Requisição sem e-mail.'})


@csrf_exempt
def getMaterias(request):
    if request.method == 'POST':
        try:
            statusMateria = request.POST['status_materia']

            if statusMateria == 'inativa':
                return getMateriasPorStatus(request, False)
            else:
                return getMateriasPorStatus(request, True)
        except:
            return JsonResponse({'status': 'error',
                                 'descricao': 'Erro ao obter lista de matérias.'})

    else:
        return JsonResponse({'status': 'error',
                             'descricao': 'Requisição sem parâmetros.'})


@csrf_exempt
def getMateriasPorStatus(request, statusMateria):
    if request.method == 'POST':
        email = request.POST['email']
        tipoUsuario = request.POST['tipo']

        if tipoUsuario == 'aluno':
            aluno = Aluno.objects.get(email=email)

            materias = []

            for materia in aluno.materias.filter(materiaAtiva=statusMateria).order_by("nomeDisciplina").order_by("-semestre").order_by("-ano"):
                materias.append({
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
                })

            return JsonResponse({
                'status': 'ok',
                'materias': materias
            })
        else:
            return JsonResponse({
                'status': 'professor'
            })
    else:
        return JsonResponse({'status': 'error',
                             'descricao': 'Requisição sem e-mail.'})


@csrf_exempt
def getMateriaPorQRCode(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']

        materia = Materia.objects.filter(codigoInscricao=codigo)

        materiaExistente = True if len(materia) > 0 else False

        if materiaExistente:
            materia = materia[0]

            if materia.materiaAtiva:
                return JsonResponse({
                    'status': 'ok',
                    'ano': materia.ano,
                    'turma': materia.turma,
                    'codigo': materia.id,
                    'semestre': materia.semestre,
                    'nome_materia': materia.nomeDisciplina,
                    'codigo_inscricao': materia.codigoInscricao,
                    'professor': {
                            'nome': materia.professor.nome,
                            'sobrenome': materia.professor.sobrenome,
                            'email': materia.professor.email,
                            'universidade': materia.professor.universidade
                        }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'descricao': 'Esta matéria está atualmente inativa.',
                    'ano': materia.ano,
                    'turma': materia.turma,
                    'codigo': materia.id,
                    'semestre': materia.semestre,
                    'nome_materia': materia.nomeDisciplina,
                    'codigo_inscricao': materia.codigoInscricao,
                    'professor': {
                        'nome': materia.professor.nome,
                        'sobrenome': materia.professor.sobrenome,
                        'email': materia.professor.email,
                        'universidade': materia.professor.universidade
                    }
                })
        else:
            return JsonResponse({
                'status': 'error',
                'descricao': 'Código não encontrado.'
            })

    else:
        return JsonResponse({
            'status': 'error',
            'descricao': 'Requisição sem código.'
        })


@csrf_exempt
def cadastrarMateria(request):
    if request.method == 'POST':
        ano = request.POST['ano']
        semestre = request.POST['semestre']
        turma = request.POST['turma']
        nomeDisciplina = request.POST['nome_disciplina']
        codigoInscricao = request.POST['codigo_inscricao']

        email_professor = request.POST['email']

        try:
            professor = Professor.objects.get(email=email_professor)
        except:
            return JsonResponse({
                'status': 'error',
                'descricao': 'Professor não cadastrado.'
            })

        nova_materia = Materia(ano=ano, semestre=semestre, turma=turma, nomeDisciplina=nomeDisciplina,
                               codigoInscricao=codigoInscricao, professor=professor)

        nova_materia.save()

        return JsonResponse({
            'status': 'ok'
        })
    else:
        return JsonResponse({
            'status': 'error',
            'descricao': 'Requisição sem e-mail'
        })


@csrf_exempt
def cancelarInscricaoEmMateria(request):
    if request.method == 'POST':
        email_aluno = request.POST['email']
        codigo_materia = request.POST['codigo']
        try:
            aluno = Aluno.objects.get(email=email_aluno)
            materia = Materia.objects.get(id=codigo_materia)
            aluno.materias.remove(materia)
            aluno.save()

            return JsonResponse({
                'status': 'ok',
            })
        except:
            return JsonResponse({
                'status': 'error',
                'descricao': 'Aluno ou matéria inválidos.',
                'email': email_aluno,
                'codigo_materia': codigo_materia,
            })
    else:
        return JsonResponse({
            'status': 'error',
            'descricao': 'Requisição sem e-mail'
        })


@csrf_exempt
def inscreverAlunoEmMateria(request):
    if request.method == 'POST':
        email_aluno = request.POST['email']
        codigo_inscricao = request.POST['codigo']

        try:
            aluno = Aluno.objects.get(email=email_aluno)
            materia = Materia.objects.get(codigoInscricao=codigo_inscricao)
            aluno.materias.add(materia)
            aluno.save()

            # TODO Tratar erro de quando a matéria já está cadastrada para este usuário
            return JsonResponse({
                'status': 'ok',
                'ano': materia.ano,
                'turma': materia.turma,
                'codigo': materia.id,
                'semestre': materia.semestre,
                'nome_materia': materia.nomeDisciplina,
                'codigo_inscricao': materia.codigoInscricao,
                'professor': {
                    'nome': materia.professor.nome,
                    'sobrenome': materia.professor.sobrenome,
                    'email': materia.professor.email,
                    'universidade': materia.professor.universidade
                }
            })
        except:
            return JsonResponse({
                'status': 'error',
                'descricao': 'Aluno ou matéria inválidos.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'descricao': 'Requisição sem e-mail'
        })

@csrf_exempt
def buscarPerfilUsuario(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            usuario = Aluno.objects.get(email=email)
            perfil = "aluno"
        except:
            try:
                usuario = Professor.objects.get(email=email)
                perfil = "professor"
            except:
                return JsonResponse({
                    'status': 'error',
                    'descricao': 'Perfil não encontrado.'
                })

        return JsonResponse({
            'status': 'ok',
            'perfil': perfil,
            'nome': usuario.nome,
            'sobrenome': usuario.sobrenome,
            'curso' if perfil == 'aluno' else 'universidade': usuario.curso if perfil == 'aluno' else usuario.universidade,
            'email': usuario.email
        })

    else:
        return JsonResponse({
            'status': 'error',
            'descricao': 'Requisição sem e-mail'
        })
