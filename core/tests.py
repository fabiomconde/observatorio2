"""
Smoke tests for the public site.

Each public URL is expected to render successfully with a sane status code
and include some site-specific text in the HTML.
"""

from django.test import TestCase, Client
from django.urls import reverse

from core.models import (
    Bioma,
    CategoriaNoticia,
    Colecao,
    Faq,
    GrupoTrabalho,
    Membro,
    MensagemContato,
    Noticia,
    Parceiro,
    Pilar,
    Publicacao,
    TermoGlossario,
    TipoPublicacao,
)


class PublicSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Garantir dados mínimos
        self.cat = CategoriaNoticia.objects.create(nome="Cobertura e Uso", cor="#0d3b66")
        self.tipo = TipoPublicacao.objects.create(nome="Relatório", cor="#0d3b66")
        self.bioma = Bioma.objects.create(
            nome="Amazônia", icone="🌳", cor="#1b5e20",
            descricao="Maior floresta tropical do mundo."
        )
        self.colecao = Colecao.objects.create(
            nome="Coleção 9", ano_inicio=1985, ano_fim=2023,
            resumo="Coleção 9 do MapBiomas", destaque=True,
        )
        self.grupo = GrupoTrabalho.objects.create(
            titulo="Recursos Hídricos", icone="bi-droplet-half", cor="#0277bd",
            descricao_curta="Análise de bacias e disponibilidade hídrica.",
        )
        self.membro = Membro.objects.create(nome="Dra. Ana Souza", funcao="Coordenadora", instituicao="UFAM")
        self.noticia = Noticia.objects.create(
            titulo="MapBiomas lança Coleção 9",
            slug="mapbiomas-lanca-colecao-9",
            resumo="Resumo teste",
            conteudo="Conteúdo de teste com mais de uma linha.\nLinha dois.",
            publicado_em="2026-08-10T12:00:00Z",
            destaque=True,
            categoria=self.cat,
        )
        self.pub = Publicacao.objects.create(
            titulo="Atlas da Cobertura da Terra",
            slug="atlas-cobertura",
            resumo="Atlas consolidado com mapas temáticos.",
            publicado_em="2024-07-01",
            tipo=self.tipo,
            destaque=True,
        )
        self.faq = Faq.objects.create(pergunta="O que é?", resposta="É um projeto.", categoria="Geral")
        self.termo = TermoGlossario.objects.create(termo="Bioma", definicao="Conjunto de ecossistemas.")
        self.pilar = Pilar.objects.create(titulo="Ciência Aberta", descricao="Scientia", icone="🔬")
        self.parceiro = Parceiro.objects.create(nome="Univ. Teste")

    def test_home(self):
        r = self.client.get(reverse("core:home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Observatório")
        self.assertContains(r, "Recursos Hídricos")
        self.assertContains(r, "Coleção 9")

    def test_quem_somos(self):
        r = self.client.get(reverse("core:quem_somos"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Quem somos")

    def test_grupos(self):
        r = self.client.get(reverse("core:grupos"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Recursos Hídricos")

    def test_grupo_detalhe(self):
        r = self.client.get(reverse("core:grupo_detalhe", args=[self.grupo.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Recursos Hídricos")

    def test_membros(self):
        r = self.client.get(reverse("core:membros"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Ana Souza")

    def test_noticias_listagem(self):
        r = self.client.get(reverse("core:noticias"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "MapBiomas lança Coleção 9")

    def test_noticias_busca(self):
        r = self.client.get(reverse("core:noticias") + "?q=Coleção")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Coleção 9")

    def test_noticia_detalhe(self):
        r = self.client.get(reverse("core:noticia_detalhe", args=[self.noticia.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "MapBiomas lança Coleção 9")

    def test_faq(self):
        r = self.client.get(reverse("core:faq"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "O que é?")

    def test_faq_categoria(self):
        r = self.client.get(reverse("core:faq") + "?categoria=Geral")
        self.assertEqual(r.status_code, 200)

    def test_glossario(self):
        r = self.client.get(reverse("core:glossario"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Bioma")

    def test_glossario_letra(self):
        r = self.client.get(reverse("core:glossario") + "?letra=B")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Bioma")

    def test_biomas(self):
        r = self.client.get(reverse("core:biomas"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Amazônia")

    def test_bioma_detalhe(self):
        r = self.client.get(reverse("core:bioma_detalhe", args=[self.bioma.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Amazônia")

    def test_colecoes(self):
        r = self.client.get(reverse("core:colecoes"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Coleção 9")

    def test_publicacoes(self):
        r = self.client.get(reverse("core:publicacoes"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Atlas da Cobertura")

    def test_publicacoes_tipo(self):
        r = self.client.get(reverse("core:publicacoes") + "?tipo=relatorio")
        self.assertEqual(r.status_code, 200)

    def test_publicacao_detalhe(self):
        r = self.client.get(reverse("core:publicacao_detalhe", args=[self.pub.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Atlas da Cobertura")

    def test_busca(self):
        r = self.client.get(reverse("core:busca") + "?q=Coleção")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "MapBiomas lança Coleção 9")

    def test_busca_vazia(self):
        r = self.client.get(reverse("core:busca"))
        self.assertEqual(r.status_code, 200)

    def test_contato_get(self):
        r = self.client.get(reverse("core:contato"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Fale conosco")

    def test_contato_post_ok(self):
        data = {
            "nome": "Maria", "email": "maria@x.org",
            "assunto": "Oi", "mensagem": "Olá!",
        }
        r = self.client.post(reverse("core:contato"), data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(MensagemContato.objects.count(), 1)

    def test_contato_post_invalido(self):
        r = self.client.post(reverse("core:contato"), {"nome": "", "email": ""})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(MensagemContato.objects.count(), 0)

    def test_404_handler(self):
        r = self.client.get("/pagina-que-nao-existe/")
        self.assertEqual(r.status_code, 404)
