from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^cadastraraluno/', cadastrarAluno, name='cadastraraluno'),
    url(r'^cadastrarprofessor/', cadastrarProfessor, name='cadastrarprofessor'),
    url(r'^buscaraluno/', getAluno, name='getaluno'),
    url(r'^buscarprofessor/', getProfessor, name='getprofessor'),
    url(r'^buscarmaterias/', getMaterias, name='getmaterias'),
    url(r'^buscarmateriaporqr/', getMateriaPorQRCode, name='getmateriasporqr'),
    url(r'^cadastrarmateria/', cadastrarMateria, name='cadastrarmateria'),
    url(r'^cancelarinscricaoemmateria/', cancelarInscricaoEmMateria, name='cancelarinscricaoemmateria'),
    url(r'^inscreveralunoemmateria/', inscreverAlunoEmMateria, name='inscreveralunoemmateria'),
    url(r'^buscarperfilusuario/', buscarPerfilUsuario, name='buscarperfilusuario'),
    url(r'^desativarmateria/', desativarMateria, name='desativarmateria'),
    url(r'^buscaralunosinscritospormateria/', getAlunosInscritosPorMateria, name='buscaralunosinscritospormateria'),
    url(r'^cadastrarpergunta/', cadastrarPergunta, name='cadastrarpergunta'),
    url(r'^buscarperguntaspormateria/', getPerguntasPorMateria, name='buscarperguntaspormateria'),
    url(r'^buscarperguntasporprofessor/', getPerguntasPorProfessor, name='buscarperguntasporprofessor'),
    url(r'^buscaralternativasporpergunta/', getAlternativasPorPergunta, name='buscaralternativasporpergunta'),
    url(r'^buscarrespostasporpergunta/', getRespostasPorPergunta, name='buscarrespostasporaluno'),
    url(r'^buscarquantidadederespostasporalternativaporpergunta/', getQuantidadeDeRespostasPorAlternativaPorPergunta, name='buscarquantidadederespostasporalternativaporpergunta')
]