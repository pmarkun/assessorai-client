from django.db import models
from django.contrib.auth.models import AbstractUser


class TimestampMixin(models.Model):
    """Mixin criado para timestamps automáticos."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ────────────────────────────────────────────────────────────────
#  Usuário / Equipe
# ────────────────────────────────────────────────────────────────
class User(AbstractUser):
    """Usuário ligado a um Mandato."""

    class Papel(models.TextChoices):
        ADMIN = "admin", "Administrador"
        GESTOR = "gestor", "Gestor"
        ASSESSOR = "assessor", "Assessor"

    funcao = models.CharField(max_length=100, blank=True, help_text="Cargo/função no mandato")
    papel = models.CharField(max_length=15, choices=Papel.choices, default=Papel.ASSESSOR)
    mandato = models.ForeignKey("Mandato", on_delete=models.CASCADE, related_name="usuarios", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


# ────────────────────────────────────────────────────────────────
#  Mandato
# ────────────────────────────────────────────────────────────────
class Mandato(TimestampMixin):
    """Dados institucionais do parlamentar."""

    class CasaLegislativa(models.TextChoices):
        CM = "cm", "Câmara Municipal"
        ALE = "ale", "Assembleia Legislativa"
        CF = "cf", "Câmara Federal"
        SENADO = "senado", "Senado Federal"

    class Cargo(models.TextChoices):
        VEREADOR = "vereador", "Vereador(a)"
        DEP_ESTADUAL = "dep_estadual", "Deputado(a) Estadual"
        DEP_FEDERAL = "dep_federal", "Deputado(a) Federal"
        SENADOR = "senador", "Senador(a)"

    class Posicionamento(models.TextChoices):
        ESQUERDA = "esq", "Esquerda"
        CENTRO_ESQ = "cesq", "Centro-esquerda"
        CENTRO = "centro", "Centro"
        CENTRO_DIR = "cdir", "Centro-direita"
        DIREITA = "dir", "Direita"

    class Perfil(models.TextChoices):
        LEGISLADOR = "legislador", "Legislador"
        FISCALIZADOR = "fiscalizador", "Fiscalizador"
        ARTICULADOR = "articulador", "Articulador"

    nome_parlamentar = models.CharField(max_length=255)
    casa_legislativa = models.CharField(max_length=10, choices=CasaLegislativa.choices)
    cargo = models.CharField(max_length=20, choices=Cargo.choices)
    estado = models.CharField(max_length=2)
    municipio = models.CharField(max_length=120, blank=True)
    posicionamento = models.CharField(max_length=6, choices=Posicionamento.choices, blank=True)
    perfil = models.CharField(max_length=15, choices=Perfil.choices, blank=True)
    primeiro_mandato = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_parlamentar


# ────────────────────────────────────────────────────────────────
#  Planejamento Estratégico
# ────────────────────────────────────────────────────────────────
class Planejamento(TimestampMixin):
    """Planejamento anual vinculado ao Mandato."""
    mandato = models.OneToOneField(Mandato, on_delete=models.CASCADE, related_name="planejamento")
    oportunidades = models.TextField(blank=True)
    fraquezas = models.TextField(blank=True)
    temas_interesse = models.TextField(blank=True)
    objetivo_ano = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Planejamento {self.mandato} {self.created_at.year}"


class Objetivo(models.Model):
    planejamento = models.ForeignKey(Planejamento, on_delete=models.CASCADE, related_name="objetivos")
    descricao = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return self.descricao


class MetaObjetivo(TimestampMixin):
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name="metas")
    indicador = models.CharField(max_length=255)
    valor_alvo = models.FloatField()
    valor_atual = models.FloatField(default=0)
    data_limite = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.indicador} (alvo {self.valor_alvo})"


# ────────────────────────────────────────────────────────────────
#  Biblioteca de Arquivos
# ────────────────────────────────────────────────────────────────
class ArquivoBiblioteca(TimestampMixin):
    class TipoArquivo(models.TextChoices):
        PDF = "pdf", "PDF"
        DOC = "doc", "DOC/DOCX"
        IMG = "img", "Imagem"
        OUTRO = "outro", "Outro"

    mandato = models.ForeignKey(Mandato, on_delete=models.CASCADE, related_name="biblioteca")
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TipoArquivo.choices)
    arquivo = models.FileField(upload_to="biblioteca/")

    def __str__(self):
        return self.titulo


# ────────────────────────────────────────────────────────────────
#  Equipe e Configurações de IA
# ────────────────────────────────────────────────────────────────
class Invitation(TimestampMixin):
    """Convite para novos membros da equipe."""

    mandato = models.ForeignKey(Mandato, on_delete=models.CASCADE, related_name="convites")
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    funcao = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.email} - {self.funcao}"


class AISettings(models.Model):
    """Configurações para acesso à API de IA."""

    api_key = models.CharField(max_length=255, blank=True)
    model_name = models.CharField(max_length=100, default="gpt-3.5-turbo")

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

