from django.contrib import admin
from .models import Cuidador, Paciente, ListaNegra

@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    # Exibimos apenas o que existe no seu models.py atual
    list_display = ('razao_social', 'nome_responsavel', 'cnpj', 'cidade', 'bairro', 'status_mei', 'em_escala')
    list_filter = ('status_mei', 'em_escala', 'cidade') # Removido o tipo_cadastro que dava erro
    search_fields = ('razao_social', 'cnpj', 'nome_responsavel')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Removido o 'cep' que dava erro
    list_display = ('nome', 'cidade', 'bairro', 'tipo_escala')
    list_filter = ('tipo_escala', 'cidade')
    search_fields = ('nome',)

@admin.register(ListaNegra)
class ListaNegraAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'motivo', 'data_bloqueio')