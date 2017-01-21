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
    url(r'^cadastrarmateria/', views.cadastrarMateria, name='cadastrarmateria'),
    url(r'^cancelarinscricaoemmateria/', views.cancelarInscricaoEmMateria, name='cancelarinscricaoemmateria'),
    url(r'^inscreveralunoemmateria/', views.inscreverAlunoEmMateria, name='inscreveralunoemmateria'),
    url(r'^buscarperfilusuario/', views.buscarPerfilUsuario, name='buscarperfilusuario'),
    url(r'^desativarmateria/', views.desativarMateria, name='desativarmateria'),
    url(r'^buscaralunosinscritospormateria/', views.getAlunosInscritosPorMateria, name='buscaralunosinscritospormateria'),
    url(r'^cadastrarpergunta/', views.cadastrarPergunta, name='cadastrarpergunta'),
    url(r'^buscarperguntaspormateria/', views.getPerguntasPorMateria, name='buscarperguntaspormateria'),
]