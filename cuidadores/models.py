from django.db import models

class ListaNegra(models.Model):
    cnpj = models.CharField("CNPJ Bloqueado", max_length=18, unique=True)
    motivo = models.TextField("Motivo do Banimento")
    data_bloqueio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Lista Negra"

class Cuidador(models.Model):
    STATUS_CHOICES = [('Ativo', 'Ativo'), ('Irregular', 'Irregular'), ('Pendente', 'Pendente')]
    nome_responsavel = models.CharField("Nome do Responsável", max_length=200)
    cnpj = models.CharField("CNPJ da Empresa", max_length=18, unique=True)
    razao_social = models.CharField("Razão Social", max_length=255, blank=True)
    email = models.EmailField("E-mail")
    telefone = models.CharField("WhatsApp", max_length=20)
    cep = models.CharField("CEP", max_length=9)
    cidade = models.CharField("Cidade", max_length=100)
    bairro = models.CharField("Bairro", max_length=100)
    logradouro = models.CharField("Endereço/Rua", max_length=200) # CAMPO OBRIGATÓRIO
    
    # ESPECIALIDADES
    sabe_sonda = models.BooleanField(default=False)
    sabe_banho_leito = models.BooleanField(default=False)
    sabe_transferencia = models.BooleanField(default=False)
    exp_alzheimer = models.BooleanField(default=False)

    nota_prova = models.IntegerField(default=0)
    status_mei = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pendente')
    doc_mei = models.FileField(upload_to='docs/mei/', null=True, blank=True)
    doc_antecedentes = models.FileField(upload_to='docs/criminais/', null=True, blank=True)
    em_escala = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.razao_social or self.nome_responsavel}"

class Paciente(models.Model):
    ESCALAS = [('12x36', '12h x 36h'), ('24x24', '24h x 24h'), ('Folguista', 'Folguista')]
    nome = models.CharField("Nome do Paciente", max_length=200)
    data_nascimento = models.DateField()
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    usa_sonda = models.BooleanField(default=False)
    requer_banho_leito = models.BooleanField(default=False)
    particularidades_pad = models.TextField()
    tipo_escala = models.CharField(max_length=20, choices=ESCALAS)
    cuidadores_direcionados = models.ManyToManyField(Cuidador, blank=True, related_name="pacientes")

    def __str__(self):
        return self.nome