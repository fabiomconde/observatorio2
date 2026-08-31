"""
Django admin registration for the public-site models.
"""

from django.contrib import admin

from .models import (
    Bioma,
    CategoriaNoticia,
    Colecao,
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


@admin.register(Bioma)
class BiomaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "atualizado_em")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "atualizado_em")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "regiao", "populacao", "area_km2", "ativo")
    list_filter = ("regiao", "tipo", "ativo")
    search_fields = ("nome", "codigo_ibge", "descricao")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ano_inicio", "ano_fim", "lancado_em", "destaque", "ativo")
    list_filter = ("destaque", "ativo")
    search_fields = ("nome", "resumo")
    prepopulated_fields = {"slug": ("nome",)}
    date_hierarchy = "lancado_em"


@admin.register(GrupoTrabalho)
class GrupoTrabalhoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "coordenador", "ordem", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao_curta", "descricao", "coordenador")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("ordem", "titulo")


@admin.register(TipoPublicacao)
class TipoPublicacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ordem", "cor")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)
    ordering = ("ordem", "nome")


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "publicado_em", "destaque", "ativo")
    list_filter = ("tipo", "destaque", "ativo", "publicado_em")
    search_fields = ("titulo", "resumo", "descricao", "autores")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "publicado_em"
    autocomplete_fields = ("tipo",)


@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cor")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "publicado_em", "destaque", "ativo")
    list_filter = ("categoria", "destaque", "ativo", "publicado_em")
    search_fields = ("titulo", "resumo", "conteudo")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "publicado_em"
    autocomplete_fields = ("categoria",)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("pergunta", "categoria", "ordem", "ativo")
    list_filter = ("ativo", "categoria")
    search_fields = ("pergunta", "resposta")
    ordering = ("ordem",)


@admin.register(TermoGlossario)
class TermoGlossarioAdmin(admin.ModelAdmin):
    list_display = ("termo", "categoria", "ativo")
    list_filter = ("ativo", "categoria")
    search_fields = ("termo", "definicao")
    prepopulated_fields = {"slug": ("termo",)}


@admin.register(Pilar)
class PilarAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ordem", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")
    ordering = ("ordem",)


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ("nome", "funcao", "instituicao", "ordem", "ativo")
    list_filter = ("ativo", "instituicao")
    search_fields = ("nome", "funcao", "instituicao", "biografia")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("ordem", "nome")


@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "ordem", "ativo")
    list_filter = ("ativo", "tipo")
    search_fields = ("nome",)
    ordering = ("ordem", "nome")


from django.utils.html import format_html


@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "assunto", "status_lida", "criado_em")
    list_filter = ("lida",)
    search_fields = ("nome", "email", "assunto", "mensagem")
    readonly_fields = ("nome", "email", "assunto", "mensagem", "criado_em")
    actions = ["marcar_como_lida"]

    @admin.display(description="Status", ordering="lida")
    def status_lida(self, obj):
        if obj.lida:
            return format_html('<span class="notion-badge notion-badge-green">✓ Lida</span>')
        return format_html('<span class="notion-badge notion-badge-yellow">● Nova</span>')

    @admin.action(description="Marcar selecionadas como lidas")
    def marcar_como_lida(self, request, queryset):
        queryset.update(lida=True)

