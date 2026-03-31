from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from cuidadores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    
    # AUTENTICAÇÃO
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # RECRUTAMENTO (PÚBLICO)
    path('recrutamento/prova/', views.entrada_prova_view, name='entrada_prova'),
    path('avaliacao/', views.fazer_prova_view, name='fazer_prova'),
    path('finalizar-cadastro/', views.cadastro_completo_view, name='cadastro_completo'),
    
    # GESTÃO (PROTEGIDO)
    path('gestao/', views.dashboard_view, name='dashboard'),
    path('gestao/alocar/<int:paciente_id>/', views.alocar_cuidador_view, name='alocar_cuidador'),
    path('gestao/revisar/<int:cuidador_id>/', views.revisar_cuidador_view, name='revisar_cuidador'),
    path('gestao/liberar/<int:paciente_id>/<int:cuidador_id>/', views.liberar_cuidador_view, name='liberar_cuidador'),
    path('gestao/relatorio/<int:paciente_id>/', views.relatorio_paciente_view, name='relatorio_paciente'),
    
    # CONSULTA (PÚBLICO)
    path('consulta/', views.consulta_escala_view, name='consulta_escala'),
]