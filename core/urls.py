"""
URL routes for the public site.
"""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),

    # O Projeto
    path("o-projeto/", views.quem_somos, name="quem_somos"),
    path("grupos-de-trabalho/", views.grupos, name="grupos"),
    path("grupos-de-trabalho/<slug:slug>/", views.grupo_detalhe, name="grupo_detalhe"),
    path("membros/", views.membros, name="membros"),

    # Dados & Mapas
    path("biomas/", views.biomas, name="biomas"),
    path("biomas/<slug:slug>/", views.bioma_detalhe, name="bioma_detalhe"),
    path("colecoes/", views.colecoes, name="colecoes"),

    # Publicações
    path("publicacoes/", views.publicacoes, name="publicacoes"),
    path("publicacoes/<slug:slug>/", views.publicacao_detalhe, name="publicacao_detalhe"),

    # Notícias
    path("noticias/", views.noticias, name="noticias"),
    path("noticias/<slug:slug>/", views.noticia_detalhe, name="noticia_detalhe"),

    # Conteúdo
    path("faq/", views.faq, name="faq"),
    path("glossario/", views.glossario, name="glossario"),

    # Busca
    path("busca/", views.busca, name="busca"),

    # Contato
    path("contato/", views.contato, name="contato"),
]
