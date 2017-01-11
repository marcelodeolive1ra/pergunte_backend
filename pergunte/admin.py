from django.contrib import admin
from .models import *

admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Materia)