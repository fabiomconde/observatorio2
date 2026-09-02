"""
Domain models for the Observatório Socioambiental app.

All entities used across the public site and the Django admin live here.
"""

import re
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract base with created/updated timestamps."""

    criado_em = models.DateTimeField(_("criado em"), auto_now_add=True)
    atualizado_em = models.DateTimeField(_("atualizado em"), auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------------------------- #
# Biomas
# --------------------------------------------------------------------- #
class Bioma(TimeStampedModel):
    """Brazilian biomes monitored by the project."""

    nome = models.CharField(_("nome"), max_length=80, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)
    descricao = models.TextField(_("descrição"), blank=True)
    icone = models.CharField(
        _("ícone (emoji)"),
        max_length=8,
        blank=True,
        help_text=_("Emoji representativo exibido no card."),
    )
    cor = models.CharField(
        _("cor (hex)"),
        max_length=7,
        default="#1d4e89",
        help_text=_("Cor de destaque em CSS, ex: #1d4e89"),
    )
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = _("Bioma")
        verbose_name_plural = _("Biomas")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


# --------------------------------------------------------------------- #
# Regiões e Distritos
# --------------------------------------------------------------------- #
class Regiao(TimeStampedModel):
    """Região territorial do município (ex: Alto Madeira, Médio Madeira, Baixo Madeira)."""

    nome = models.CharField(_("nome"), max_length=80, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)
    descricao = models.TextField(_("descrição"), blank=True)
    icone = models.CharField(
        _("ícone (Bootstrap Icons)"),
        max_length=40,
        default="bi-map",
        blank=True,
    )
    cor = models.CharField(_("cor (hex)"), max_length=7, default="#0d3b66")
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = _("Região")
        verbose_name_plural = _("Regiões")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Distrito(TimeStampedModel):
    """Distritos do município de Porto Velho/RO."""

    nome = models.CharField(_("nome"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), max_length=120, unique=True, blank=True)
    codigo_ibge = models.CharField(_("código IBGE"), max_length=20, blank=True)
    tipo = models.CharField(_("tipo"), max_length=40, default="Distrito")
    populacao = models.PositiveIntegerField(_("população"), null=True, blank=True)
    domicilios = models.PositiveIntegerField(_("domicílios"), null=True, blank=True)
    area_km2 = models.FloatField(_("área (km²)"), null=True, blank=True)
    densidade = models.FloatField(_("densidade demográfica (hab/km²)"), null=True, blank=True)
    regiao = models.ForeignKey(
        Regiao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="distritos",
        verbose_name=_("região"),
    )
    criacao = models.CharField(_("data/ano de criação"), max_length=60, blank=True)
    distancia_sede_km = models.PositiveIntegerField(_("distância da sede (km)"), null=True, blank=True)
    descricao = models.TextField(_("descrição"), blank=True)
    tags = models.JSONField(_("tags / palavras-chave"), default=list, blank=True)
    icone = models.CharField(_("ícone (emoji ou BI)"), max_length=40, default="bi-geo-alt", blank=True)
    cor = models.CharField(_("cor (hex)"), max_length=7, default="#1d4e89")
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["-populacao", "nome"]
        verbose_name = _("Distrito")
        verbose_name_plural = _("Distritos")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome

    @property
    def populacao_formatada(self) -> str:
        if self.populacao is None:
            return "—"
        return f"{self.populacao:,}".replace(",", ".")

    @property
    def domicilios_formatados(self) -> str:
        if self.domicilios is None:
            return "—"
        return f"{self.domicilios:,}".replace(",", ".")

    @property
    def area_formatada(self) -> str:
        if self.area_km2 is None:
            return "—"
        val = self.area_km2
        if val == int(val):
            return f"{int(val):,}".replace(",", ".")
        formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted.rstrip("0").rstrip(",")

    @property
    def densidade_formatada(self) -> str:
        if self.densidade is None:
            return "—"
        val = self.densidade
        if val == int(val):
            return f"{int(val):,}".replace(",", ".")
        formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted.rstrip("0").rstrip(",")


# --------------------------------------------------------------------- #
# Coleções / Datasets
# --------------------------------------------------------------------- #
class Colecao(TimeStampedModel):
    """Annual Observatório Socioambiental collection (a snapshot of all maps for a year)."""

    nome = models.CharField(_("nome"), max_length=120, unique=True)
    slug = models.SlugField(_("slug"), max_length=140, unique=True, blank=True)
    ano_inicio = models.PositiveSmallIntegerField(_("ano inicial"))
    ano_fim = models.PositiveSmallIntegerField(_("ano final"))
    resumo = models.TextField(_("resumo"), blank=True)
    lancado_em = models.DateField(_("lançado em"), null=True, blank=True)
    destaque = models.BooleanField(_("destaque"), default=False)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["-lancado_em", "-ano_fim"]
        verbose_name = _("Coleção")
        verbose_name_plural = _("Coleções")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nome} ({self.ano_inicio}–{self.ano_fim})"

    @property
    def anos_cobertura(self) -> int:
        return max(0, (self.ano_fim or 0) - (self.ano_inicio or 0) + 1)


# --------------------------------------------------------------------- #
# Grupos de Trabalho (estilo "GTs" do Observatório RMM)
# --------------------------------------------------------------------- #
class GrupoTrabalho(TimeStampedModel):
    """Working groups / research axes that drive the observatory."""

    titulo = models.CharField(_("título"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True, blank=True)
    descricao_curta = models.CharField(
        _("descrição curta"), max_length=200, blank=True,
        help_text=_("Até 200 caracteres — exibida nos cards."),
    )
    descricao = models.TextField(_("descrição completa"), blank=True)
    icone = models.CharField(
        _("ícone (Bootstrap Icons name)"),
        max_length=40,
        blank=True,
        help_text=_("Ex: bi-droplet, bi-tree, bi-cloud-rain"),
    )
    cor = models.CharField(_("cor (hex)"), max_length=7, default="#0d3b66")
    coordenador = models.CharField(_("coordenador(a)"), max_length=120, blank=True)
    ordem = models.PositiveIntegerField(_("ordem"), default=0)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "titulo"]
        verbose_name = _("Grupo de Trabalho")
        verbose_name_plural = _("Grupos de Trabalho")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo


# --------------------------------------------------------------------- #
# Publicações (relatórios, artigos, legislação, notas técnicas)
# --------------------------------------------------------------------- #
class TipoPublicacao(TimeStampedModel):
    """Tipo/categoria da publicação (Relatório, Artigo, Legislação, etc.)."""

    nome = models.CharField(_("nome"), max_length=80, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)
    icone = models.CharField(
        _("ícone (Bootstrap Icons)"),
        max_length=40,
        default="bi-file-earmark-text",
    )
    cor = models.CharField(_("cor (hex)"), max_length=7, default="#0d3b66")
    ordem = models.PositiveIntegerField(_("ordem"), default=0)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = _("Tipo de publicação")
        verbose_name_plural = _("Tipos de publicação")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Publicacao(TimeStampedModel):
    """Publicação técnica: relatório, artigo, legislação, etc."""

    titulo = models.CharField(_("título"), max_length=220)
    slug = models.SlugField(_("slug"), max_length=240, unique=True, blank=True)
    resumo = models.TextField(_("resumo"), blank=True)
    descricao = models.TextField(_("descrição completa"), blank=True)
    tipo = models.ForeignKey(
        TipoPublicacao,
        on_delete=models.PROTECT,
        related_name="publicacoes",
        verbose_name=_("tipo"),
    )
    autores = models.CharField(_("autores"), max_length=300, blank=True)
    publicado_em = models.DateField(_("data"), null=True, blank=True)
    arquivo = models.FileField(
        _("arquivo (PDF)"),
        upload_to="publicacoes/",
        blank=True,
        null=True,
    )
    link_externo = models.URLField(_("link externo"), blank=True)
    imagem = models.ImageField(
        _("imagem de capa"),
        upload_to="publicacoes/capas/",
        blank=True,
        null=True,
    )
    destaque = models.BooleanField(_("destaque na home"), default=False)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["-publicado_em", "-criado_em"]
        verbose_name = _("Publicação")
        verbose_name_plural = _("Publicações")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:220] or "publicacao"
            slug = base
            i = 1
            while Publicacao.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo


# --------------------------------------------------------------------- #
# Notícias
# --------------------------------------------------------------------- #
class CategoriaNoticia(TimeStampedModel):
    nome = models.CharField(_("nome"), max_length=60, unique=True)
    slug = models.SlugField(_("slug"), max_length=80, unique=True, blank=True)
    cor = models.CharField(_("cor (hex)"), max_length=7, default="#0d3b66")

    class Meta:
        ordering = ["nome"]
        verbose_name = _("Categoria de notícia")
        verbose_name_plural = _("Categorias de notícia")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Noticia(TimeStampedModel):
    titulo = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True, blank=True)
    resumo = models.TextField(_("resumo"), max_length=400, blank=True)
    conteudo = models.TextField(_("conteúdo"))
    imagem = models.ImageField(
        _("imagem de capa"),
        upload_to="noticias/",
        blank=True,
        null=True,
    )
    categoria = models.ForeignKey(
        CategoriaNoticia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="noticias",
        verbose_name=_("categoria"),
    )
    publicado_em = models.DateTimeField(_("publicado em"), null=True, blank=True)
    destaque = models.BooleanField(_("destaque na home"), default=False)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["-publicado_em", "-criado_em"]
        verbose_name = _("Notícia")
        verbose_name_plural = _("Notícias")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200] or "noticia"
            slug = base
            i = 1
            while Noticia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo


# --------------------------------------------------------------------- #
# FAQ
# --------------------------------------------------------------------- #
class Faq(TimeStampedModel):
    categoria = models.CharField(_("categoria"), max_length=80, blank=True)
    pergunta = models.CharField(_("pergunta"), max_length=250)
    resposta = models.TextField(_("resposta"))
    ordem = models.PositiveIntegerField(_("ordem"), default=0)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "pergunta"]
        verbose_name = _("Pergunta Frequente")
        verbose_name_plural = _("Perguntas Frequentes")

    def __str__(self) -> str:
        return self.pergunta


# --------------------------------------------------------------------- #
# Glossário
# --------------------------------------------------------------------- #
class TermoGlossario(TimeStampedModel):
    termo = models.CharField(_("termo"), max_length=80, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)
    definicao = models.TextField(_("definição"))
    categoria = models.CharField(_("categoria"), max_length=80, blank=True)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["termo"]
        verbose_name = _("Termo do glossário")
        verbose_name_plural = _("Termos do glossário")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.termo)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.termo


# --------------------------------------------------------------------- #
# Pilares / Equipe / Parceiros
# --------------------------------------------------------------------- #
class Pilar(TimeStampedModel):
    """Top-level 'About' pillars: science, technology, transparency, etc."""

    titulo = models.CharField(_("título"), max_length=120)
    icone = models.CharField(_("ícone (emoji)"), max_length=8, blank=True)
    descricao = models.TextField(_("descrição"))
    ordem = models.PositiveIntegerField(_("ordem"), default=0)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "titulo"]
        verbose_name = _("Pilar")
        verbose_name_plural = _("Pilares")

    def __str__(self) -> str:
        return self.titulo


class Membro(TimeStampedModel):
    """Team members (membros do observatório)."""

    nome = models.CharField(_("nome"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True, blank=True)
    funcao = models.CharField(_("função / cargo"), max_length=120, blank=True)
    instituicao = models.CharField(_("instituição"), max_length=180, blank=True)
    biografia = models.TextField(_("biografia"), blank=True)
    foto = models.ImageField(_("foto"), upload_to="membros/", blank=True, null=True)
    email = models.EmailField(_("e-mail"), blank=True)
    link_lattes = models.URLField(_("Lattes"), blank=True)
    ordem = models.PositiveIntegerField(_("ordem"), default=0)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = _("Membro")
        verbose_name_plural = _("Membros")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Parceiro(TimeStampedModel):
    nome = models.CharField(_("nome"), max_length=120, unique=True)
    site = models.URLField(_("site"), blank=True)
    tipo = models.CharField(
        _("tipo"),
        max_length=40,
        blank=True,
        help_text=_("ex: universidade, ONG, empresa de tecnologia"),
    )
    logo = models.ImageField(
        _("logo"),
        upload_to="parceiros/",
        blank=True,
        null=True,
    )
    ordem = models.PositiveIntegerField(_("ordem"), default=0)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = _("Parceiro")
        verbose_name_plural = _("Parceiros")

    def __str__(self) -> str:
        return self.nome


# --------------------------------------------------------------------- #
# Contato (mensagens enviadas pelo formulário público)
# --------------------------------------------------------------------- #
class MensagemContato(TimeStampedModel):
    nome = models.CharField(_("nome"), max_length=120)
    email = models.EmailField(_("e-mail"))
    assunto = models.CharField(_("assunto"), max_length=200)
    mensagem = models.TextField(_("mensagem"))
    lida = models.BooleanField(_("lida"), default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = _("Mensagem de contato")
        verbose_name_plural = _("Mensagens de contato")

    def __str__(self) -> str:
        return f"{self.nome} <{self.email}> — {self.assunto}"


def _format_mobile_url(url: str) -> str:
    """Ajusta a URL para economizar espaço e otimizar a exibição em mobile: standalone=2 e show_filters=0."""
    url = url.strip()
    if not url:
        return ""
    if re.search(r"standalone=(1|true|0)", url):
        url = re.sub(r"standalone=(1|true|0)", "standalone=2", url)
    elif "standalone=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}standalone=2"

    if "show_filters=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}show_filters=0"
    return url


# --------------------------------------------------------------------- #
# Dashboards Públicos (Apache Superset ou outros iFrames)
# --------------------------------------------------------------------- #
class Dashboard(TimeStampedModel):
    """Dashboards de indicadores públicos embutidos via iframe (ex: Apache Superset)."""

    titulo = models.CharField(_("título"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=160, unique=True, blank=True)
    descricao = models.TextField(_("descrição"), blank=True)
    link = models.URLField(
        _("link / URL do iframe (Desktop)"),
        max_length=500,
        help_text=_("URL pública do dashboard para Desktop, ex: https://painel.provaconceito.tech/superset/dashboard/.../?standalone=1"),
    )
    link_responsivo = models.URLField(
        _("link / URL do iframe (Mobile)"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("URL pública do dashboard para Mobile (ex: https://painel.provaconceito.tech/superset/dashboard/.../?standalone=2&show_filters=0). Se não preenchida, é gerada automaticamente no salvar."),
    )
    icone = models.CharField(
        _("ícone (Bootstrap Icons)"),
        max_length=40,
        default="bi-bar-chart-line",
        blank=True,
    )
    ordem = models.PositiveIntegerField(_("ordem de exibição"), default=0)
    destaque = models.BooleanField(_("destaque"), default=False)
    ativo = models.BooleanField(_("ativo"), default=True)

    class Meta:
        ordering = ["ordem", "-criado_em"]
        verbose_name = _("Dashboard")
        verbose_name_plural = _("Dashboards")

    @property
    def link_standalone(self) -> str:
        url = (self.link or "").strip()
        if not url:
            return ""
        if "standalone=" in url:
            return url
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}standalone=1"

    def get_url_for_request(self, request) -> str:
        """Retorna a URL adequada dependendo do dispositivo (Mobile/Tablet vs Desktop)."""
        if hasattr(request, "user_agent") and (request.user_agent.is_mobile or request.user_agent.is_tablet):
            return self.link_responsivo or self.link_standalone or self.link
        return self.link_standalone or self.link

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)

        if self.link:
            self.link = self.link.strip()
            if "standalone=" not in self.link:
                sep = "&" if "?" in self.link else "?"
                self.link = f"{self.link}{sep}standalone=2"

        if not self.link_responsivo:
            if self.link:
                self.link_responsivo = _format_mobile_url(self.link)
        else:
            self.link_responsivo = _format_mobile_url(self.link_responsivo)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo

