from django.conf.urls import include, url
from pergunte import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastraraluno/', views.cadastrarAluno, name='cadastraraluno'),
    url(r'^cadastrarprofessor/', views.cadastrarProfessor, name='cadastrarprofessor'),
    url(r'^buscaraluno/', views.getAluno, name='getaluno'),
    url(r'^buscarprofessor/', views.getProfessor, name='getprofessor'),
    url(r'^buscarmaterias/', views.getMaterias, name='getmaterias'),
    url(r'^buscarmateriaporqr/', views.getMateriaPorQRCode, name='getmateriasporqr'),
]