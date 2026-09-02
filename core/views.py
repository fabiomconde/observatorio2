"""
Public-facing views for the Observatório Socioambiental.

Each view is a thin wrapper that fetches data from the ORM and delegates
rendering to a template. There is no business logic here.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import (
    Bioma,
    CategoriaNoticia,
    Colecao,
    Dashboard,
    Distrito,
    Faq,
    GrupoTrabalho,
    Membro,
    MensagemContato,
    Noticia,
    Parceiro,
    Pilar,
    Publicacao,
    Regiao,
    TermoGlossario,
    TipoPublicacao,
)


# --------------------------------------------------------------------- #
# Home
# --------------------------------------------------------------------- #
def home(request):
    """Landing page."""
    context = {
        "destaques": Noticia.objects.filter(ativo=True, destaque=True)
        .select_related("categoria")
        .order_by("-publicado_em")[:3],
        "ultimas_noticias": Noticia.objects.filter(ativo=True)
        .select_related("categoria")
        .order_by("-publicado_em")[:4],
        "grupos": GrupoTrabalho.objects.filter(ativo=True)[:7],
        "colecao_destaque": Colecao.objects.filter(ativo=True, destaque=True).first(),
        "publicacoes_destaque": Publicacao.objects.filter(ativo=True, destaque=True)
        .select_related("tipo")
        .order_by("-publicado_em")[:3],
        "ultimas_publicacoes": Publicacao.objects.filter(ativo=True)
        .select_related("tipo")
        .order_by("-publicado_em")[:6],
        "parceiros": Parceiro.objects.filter(ativo=True)[:12],
        "tipos_publicacao": TipoPublicacao.objects.all(),
    }
    return render(request, "core/home.html", context)


# --------------------------------------------------------------------- #
# O Projeto / Quem Somos
# --------------------------------------------------------------------- #
def quem_somos(request):
    context = {
        "pilares": Pilar.objects.filter(ativo=True),
        "parceiros": Parceiro.objects.filter(ativo=True),
        "grupos": GrupoTrabalho.objects.filter(ativo=True),
    }
    return render(request, "core/quem_somos.html", context)


def grupos(request):
    return render(
        request,
        "core/grupos.html",
        {"grupos": GrupoTrabalho.objects.filter(ativo=True)},
    )


def grupo_detalhe(request, slug):
    grupo = get_object_or_404(GrupoTrabalho, slug=slug, ativo=True)
    relacionados = (
        GrupoTrabalho.objects.filter(ativo=True)
        .exclude(pk=grupo.pk)
        .order_by("ordem")[:3]
    )
    return render(
        request,
        "core/grupo_detalhe.html",
        {"grupo": grupo, "relacionados": relacionados},
    )


def membros(request):
    return render(
        request,
        "core/membros.html",
        {"membros": Membro.objects.filter(ativo=True)},
    )


# --------------------------------------------------------------------- #
# Dados & Mapas
# --------------------------------------------------------------------- #
def biomas(request):
    biomas = Bioma.objects.filter(ativo=True)
    return render(request, "core/biomas.html", {"biomas": biomas})


def bioma_detalhe(request, slug):
    bioma = get_object_or_404(Bioma, slug=slug, ativo=True)
    return render(request, "core/bioma_detalhe.html", {"bioma": bioma})


def distritos(request):
    regiao_slug = request.GET.get("regiao", "").strip()
    termo = request.GET.get("q", "").strip()

    qs = Distrito.objects.filter(ativo=True).select_related("regiao")
    if regiao_slug:
        qs = qs.filter(regiao__slug=regiao_slug)
    if termo:
        qs = qs.filter(
            Q(nome__icontains=termo)
            | Q(descricao__icontains=termo)
            | Q(tags__icontains=termo)
        )

    regioes = Regiao.objects.filter(ativo=True)
    pop_total = sum(d.populacao for d in qs if d.populacao)

    indicadores = [
        {
            "titulo": "Distritos",
            "valor": qs.count(),
            "unidade": "distritos oficiais",
            "icone": "bi-geo-alt",
            "descricao": "Distritos de Porto Velho/RO.",
        },
        {
            "titulo": "População Total",
            "valor": f"{pop_total:,}".replace(",", "."),
            "unidade": "habitantes",
            "icone": "bi-people",
            "descricao": "População nos distritos selecionados.",
        },
        {
            "titulo": "Regiões",
            "valor": regioes.count(),
            "unidade": "regiões territoriais",
            "icone": "bi-map",
            "descricao": "Alto Madeira, Médio Madeira e Baixo Madeira.",
        },
        {
            "titulo": "Área municipal",
            "valor": "34.091",
            "unidade": "km²",
            "icone": "bi-bounding-box",
            "descricao": "Área territorial de Porto Velho em 2024.",
        },
    ]

    context = {
        "distritos": qs,
        "regioes": regioes,
        "regiao_ativa": regiao_slug,
        "termo": termo,
        "indicadores": indicadores,
    }
    return render(request, "core/distritos.html", context)


def distrito_detalhe(request, slug):
    distrito = get_object_or_404(
        Distrito.objects.select_related("regiao"), slug=slug, ativo=True
    )
    relacionados = (
        Distrito.objects.filter(ativo=True)
        .exclude(pk=distrito.pk)
        .order_by("-populacao")[:4]
    )
    dimensoes = [
        "Conflitos Agrários, Fundiários e Territoriais",
        "Pressões Ambientais, Mudanças Climáticas e Justiça Climática",
        "Violências, Segurança Pública e Direitos Humanos",
        "Dinâmicas Econômicas, Produtivas e Conflitos Socioambientais",
        "Respostas Institucionais e Políticas Públicas",
    ]
    return render(
        request,
        "core/distrito_detalhe.html",
        {
            "distrito": distrito,
            "relacionados": relacionados,
            "dimensoes": dimensoes,
        },
    )


def colecoes(request):
    colecoes = Colecao.objects.filter(ativo=True)
    return render(request, "core/colecoes.html", {"colecoes": colecoes})


# --------------------------------------------------------------------- #
# Publicações
# --------------------------------------------------------------------- #
def publicacoes(request):
    qs = Publicacao.objects.filter(ativo=True).select_related("tipo")
    tipo = request.GET.get("tipo", "").strip()
    termo = request.GET.get("q", "").strip()

    if tipo:
        qs = qs.filter(tipo__slug=tipo)
    if termo:
        qs = qs.filter(
            Q(titulo__icontains=termo)
            | Q(resumo__icontains=termo)
            | Q(autores__icontains=termo)
        )

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "core/publicacoes.html",
        {
            "page_obj": page_obj,
            "tipos": TipoPublicacao.objects.all(),
            "tipo_ativo": tipo,
            "termo": termo,
        },
    )


def publicacao_detalhe(request, slug):
    pub = get_object_or_404(Publicacao, slug=slug, ativo=True)
    relacionadas = (
        Publicacao.objects.filter(ativo=True, tipo=pub.tipo)
        .exclude(pk=pub.pk)
        .order_by("-publicado_em")[:3]
    )
    return render(
        request,
        "core/publicacao_detalhe.html",
        {"pub": pub, "relacionadas": relacionadas},
    )


# --------------------------------------------------------------------- #
# Notícias
# --------------------------------------------------------------------- #
def noticias(request):
    qs = Noticia.objects.filter(ativo=True).select_related("categoria")
    termo = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()

    if termo:
        qs = qs.filter(Q(titulo__icontains=termo) | Q(resumo__icontains=termo))
    if categoria:
        qs = qs.filter(categoria__slug=categoria)

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categorias": CategoriaNoticia.objects.all(),
        "termo": termo,
        "categoria_ativa": categoria,
    }
    return render(request, "core/noticias.html", context)


def noticia_detalhe(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug, ativo=True)
    relacionadas = (
        Noticia.objects.filter(ativo=True)
        .exclude(pk=noticia.pk)
        .order_by("-publicado_em")[:3]
    )
    return render(
        request,
        "core/noticia_detalhe.html",
        {"noticia": noticia, "relacionadas": relacionadas},
    )


# --------------------------------------------------------------------- #
# FAQ
# --------------------------------------------------------------------- #
def faq(request):
    categoria = request.GET.get("categoria", "").strip()
    qs = Faq.objects.filter(ativo=True)
    if categoria:
        qs = qs.filter(categoria__iexact=categoria)

    categorias = (
        Faq.objects.filter(ativo=True)
        .exclude(categoria="")
        .values_list("categoria", flat=True)
        .distinct()
        .order_by("categoria")
    )

    return render(
        request,
        "core/faq.html",
        {"perguntas": qs, "categorias": categorias, "categoria_ativa": categoria},
    )


# --------------------------------------------------------------------- #
# Glossário
# --------------------------------------------------------------------- #
def glossario(request):
    letra = request.GET.get("letra", "").strip().upper()
    qs = TermoGlossario.objects.filter(ativo=True)
    if letra:
        qs = qs.filter(termo__istartswith=letra)

    termos_por_letra = {}
    for t in qs:
        primeira = (t.termo[:1] or "#").upper()
        termos_por_letra.setdefault(primeira, []).append(t)

    alfabeto = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
    return render(
        request,
        "core/glossario.html",
        {
            "termos_por_letra": termos_por_letra,
            "letra_ativa": letra,
            "alfabeto": alfabeto,
            "total_termos": qs.count(),
        },
    )


# --------------------------------------------------------------------- #
# Busca global
# --------------------------------------------------------------------- #
def busca(request):
    termo = (request.GET.get("q") or "").strip()
    noticias = []
    publicacoes = []
    if termo:
        noticias = Noticia.objects.filter(ativo=True).filter(
            Q(titulo__icontains=termo) | Q(resumo__icontains=termo) | Q(conteudo__icontains=termo)
        )[:20]
        publicacoes = Publicacao.objects.filter(ativo=True).filter(
            Q(titulo__icontains=termo) | Q(resumo__icontains=termo) | Q(autores__icontains=termo)
        )[:20]
    return render(
        request,
        "core/busca.html",
        {"termo": termo, "noticias": noticias, "publicacoes": publicacoes},
    )


# --------------------------------------------------------------------- #
# Contato
# --------------------------------------------------------------------- #
@require_http_methods(["GET", "POST"])
def contato(request):
    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        email = (request.POST.get("email") or "").strip()
        assunto = (request.POST.get("assunto") or "").strip()
        mensagem_texto = (request.POST.get("mensagem") or "").strip()

        if not (nome and email and assunto and mensagem_texto):
            messages.error(request, "Por favor, preencha todos os campos.")
        else:
            MensagemContato.objects.create(
                nome=nome, email=email, assunto=assunto, mensagem=mensagem_texto
            )
            messages.success(request, "Mensagem enviada! Em breve entraremos em contato.")
            return redirect(reverse("core:contato") + "?ok=1")

    return render(request, "core/contato.html")


# --------------------------------------------------------------------- #
# Dashboards Públicos (Apache Superset)
# --------------------------------------------------------------------- #
def dashboards(request):
    """Lista de dashboards de indicadores disponíveis publicamente."""
    dashboards_list = Dashboard.objects.filter(ativo=True)
    return render(
        request,
        "core/dashboards.html",
        {"dashboards": dashboards_list},
    )


def dashboard_detalhe(request, pk):
    """Exibe o dashboard selecionado pelo ID integrado ao layout do portal."""
    dashboard = get_object_or_404(Dashboard, pk=pk, ativo=True)
    outros = Dashboard.objects.filter(ativo=True).exclude(pk=dashboard.pk)[:5]

    # Detecta se é celular ou tablet para utilizar a URL responsiva
    url_dashboard = dashboard.get_url_for_request(request)

    return render(
        request,
        "core/dashboard_detalhe.html",
        {
            "dashboard": dashboard,
            "url_dashboard": url_dashboard,
            "outros": outros,
        },
    )


def dashboard_embed(request, pk):
    """
    Exibe SOMENTE o iframe do dashboard selecionado via ID.
    Template minimalista e anônimo, sem navbar, header ou necessidade de autenticação.
    """
    dashboard = get_object_or_404(Dashboard, pk=pk, ativo=True)
    url_dashboard = dashboard.get_url_for_request(request)

    return render(
        request,
        "core/dashboard_embed.html",
        {
            "dashboard": dashboard,
            "url_dashboard": url_dashboard,
        },
    )


# --------------------------------------------------------------------- #
# Error handlers
# --------------------------------------------------------------------- #

def error_404(request, exception=None):
    return render(request, "core/404.html", status=404)


def error_500(request):
    return render(request, "core/500.html", status=500)
