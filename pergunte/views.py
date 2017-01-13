from django.shortcuts import render
from .models import Pessoa, Professor, Aluno, Materia
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
