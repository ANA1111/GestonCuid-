from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cuidador, ListaNegra, Paciente

# --- ÁREA PÚBLICA ---

def home_view(request):
    return render(request, 'cuidadores/home.html')

def entrada_prova_view(request):
    if request.method == 'POST':
        request.session['candidato_nome'] = request.POST.get('nome')
        request.session['candidato_cnpj'] = request.POST.get('cnpj')
        return redirect('fazer_prova')
    return render(request, 'cuidadores/entrada_prova.html')

def fazer_prova_view(request):
    if request.method == 'POST':
        gabarito = {'q1':'b','q2':'a','q3':'c','q4':'b','q5':'a','q6':'d','q7':'b','q8':'c','q9':'a','q10':'b'}
        nota = sum(1 for q, r in gabarito.items() if request.POST.get(q) == r)
        request.session['nota_final'] = nota
        return redirect('cadastro_completo') if nota >= 7 else redirect('home')
    return render(request, 'cuidadores/prova.html')

def cadastro_completo_view(request):
    cnpj_sessao = request.session.get('candidato_cnpj')
    if not cnpj_sessao: return redirect('home')
    if request.method == 'POST':
        if Cuidador.objects.filter(cnpj=cnpj_sessao).exists():
            messages.warning(request, "Este CNPJ já está cadastrado.")
            return redirect('home')
        Cuidador.objects.create(
            nome_responsavel=request.session.get('candidato_nome'),
            cnpj=cnpj_sessao,
            razao_social=request.POST.get('razao_social'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            cep=request.POST.get('cep'),
            cidade=request.POST.get('cidade'),
            bairro=request.POST.get('bairro'),
            logradouro=request.POST.get('logradouro'),
            sabe_sonda=request.POST.get('sabe_sonda') == 'on',
            sabe_banho_leito=request.POST.get('sabe_banho_leito') == 'on',
            sabe_transferencia=request.POST.get('sabe_transferencia') == 'on',
            exp_alzheimer=request.POST.get('exp_alzheimer') == 'on',
            nota_prova=request.session.get('nota_final', 0),
            doc_mei=request.FILES.get('doc_mei'),
            doc_antecedentes=request.FILES.get('doc_antecedentes')
        )
        request.session.flush()
        messages.success(request, "Cadastro enviado com sucesso!")
        return redirect('home')
    return render(request, 'cuidadores/cadastro.html', {'cnpj': cnpj_sessao})

def consulta_escala_view(request):
    resultado = None
    if request.method == 'POST':
        cnpj_busca = request.POST.get('cnpj')
        cuidador = Cuidador.objects.filter(cnpj=cnpj_busca).first()
        if cuidador:
            paciente = Paciente.objects.filter(cuidadores_direcionados=cuidador).first()
            resultado = {'cuidador': cuidador, 'paciente': paciente}
            if not paciente:
                messages.info(request, "Você não possui escala ativa no momento.")
        else:
            messages.error(request, "CNPJ não encontrado ou pendente de aprovação.")
    return render(request, 'cuidadores/consulta_escala.html', {'resultado': resultado})

# --- ÁREA RESTRITA (GESTÃO) ---

@login_required
def dashboard_view(request):
    context = {
        'escalados': Cuidador.objects.filter(em_escala=True).count(),
        'disponiveis': Cuidador.objects.filter(em_escala=False, status_mei='Ativo').count(),
        'pacientes_ativos': Paciente.objects.all(),
        'ultimos_cadastros': Cuidador.objects.all().order_by('-data_cadastro'),
    }
    return render(request, 'cuidadores/dashboard.html', context)

@login_required
def alocar_cuidador_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    base_cuidadores = Cuidador.objects.filter(em_escala=False, status_mei='Ativo')
    cuidadores_locais = base_cuidadores.filter(cidade__iexact=paciente.cidade, bairro__iexact=paciente.bairro)
    outros_cuidadores = base_cuidadores.filter(cidade__iexact=paciente.cidade).exclude(id__in=cuidadores_locais)
    if request.method == 'POST':
        c_id = request.POST.get('cuidador_id')
        if c_id:
            cuidador = get_object_or_404(Cuidador, id=c_id)
            paciente.cuidadores_direcionados.add(cuidador)
            cuidador.em_escala = True
            cuidador.save()
            return redirect('dashboard')
    return render(request, 'cuidadores/alocar.html', {'paciente': paciente, 'cuidadores_locais': cuidadores_locais, 'outros_cuidadores': outros_cuidadores})

@login_required
def liberar_cuidador_view(request, paciente_id, cuidador_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    cuidador = get_object_or_404(Cuidador, id=cuidador_id)
    paciente.cuidadores_direcionados.remove(cuidador)
    cuidador.em_escala = False
    cuidador.save()
    return redirect('dashboard')

@login_required
def revisar_cuidador_view(request, cuidador_id):
    cuidador = get_object_or_404(Cuidador, id=cuidador_id)
    if request.method == 'POST':
        cuidador.status_mei = request.POST.get('status_mei')
        cuidador.save()
        return redirect('dashboard')
    return render(request, 'cuidadores/revisar.html', {'cuidador': cuidador})

@login_required
def relatorio_paciente_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'cuidadores/relatorio_paciente.html', {'paciente': paciente, 'equipe': paciente.cuidadores_direcionados.all()})