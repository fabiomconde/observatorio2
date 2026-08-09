"""
Idempotent seed command — populates the database with MapBiomas-flavored
demo data so the project is browsable on a fresh install.
"""

from datetime import date, datetime, timezone

from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Popula o banco com dados de demonstração (idempotente)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🌱 Populando dados de demonstração…"))

        # ---- Biomas ------------------------------------------------------ #
        biomas = [
            ("Amazônia", "🌳", "#1b5e20",
             "Maior floresta tropical do mundo, abriga enorme biodiversidade e regula o clima global."),
            ("Cerrado", "🌿", "#f9a825",
             "Savana brasileira considerada a mais biodiversa do mundo; berço das águas."),
            ("Mata Atlântica", "🌲", "#2e7d32",
             "Floresta tropical úmida que se estendia originalmente por quase todo o litoral brasileiro."),
            ("Caatinga", "☀️", "#bf6f2a",
             "Bioma exclusivamente brasileiro, adaptado a climas semiáridos."),
            ("Pampa", "🌾", "#9ccc65",
             "Pradaria no sul do Brasil, com rica fauna e pecuária extensiva."),
            ("Pantanal", "💧", "#0277bd",
             "Maior planície alagável do planeta, hotspot de biodiversidade."),
        ]
        for nome, icone, cor, desc in biomas:
            Bioma.objects.update_or_create(
                nome=nome,
                defaults=dict(icone=icone, cor=cor, descricao=desc, ativo=True),
            )

        # ---- Coleções ---------------------------------------------------- #
        colecoes = [
            ("Coleção 9", 1985, 2023, date(2024, 7, 1), True,
             "A Coleção 9 amplia a cobertura temporal até 2023, com novos mapas e estatísticas "
             "para os seis biomas brasileiros."),
            ("Coleção 8", 1985, 2022, date(2023, 8, 1), False,
             "Coleção 8 — mapas anuais até 2022, com módulos de fogo e água."),
            ("Coleção 7", 1985, 2021, date(2022, 8, 1), False,
             "Coleção 7 — inclusão de módulos de pastagem e agricultura."),
        ]
        for nome, ini, fim, lanc, destaque, resumo in colecoes:
            Colecao.objects.update_or_create(
                nome=nome,
                defaults=dict(
                    ano_inicio=ini, ano_fim=fim, lancado_em=lanc,
                    destaque=destaque, resumo=resumo, ativo=True,
                ),
            )

        # ---- Grupos de Trabalho ---------------------------------------- #
        grupos = [
            ("Recursos Hídricos", "bi-droplet-half", "#0277bd",
             "Análise de bacias, qualidade da água e disponibilidade hídrica no território.",
             "Monitoramento de bacias hidrográficas, qualidade da água e disponibilidade para abastecimento, "
             "irrigação e geração de energia.",
             "Dra. Ana Souza", 1),
            ("Mudanças Climáticas", "bi-cloud-rain", "#1d4e89",
             "Riscos climáticos, emissões e adaptação nos biomas brasileiros.",
             "Estudo de cenários climáticos, emissões de GEE e estratégias de adaptação em nível regional.",
             "Dr. Carlos Lima", 2),
            ("Cobertura e Uso da Terra", "bi-globe-americas", "#2e7d32",
             "Mapeamento anual da cobertura vegetal e uso do solo desde 1985.",
             "Geração dos mapas anuais de cobertura e uso da terra, em parceria com universidades e ONGs.",
             "Dra. Beatriz Alves", 3),
            ("Fogo e Cicatrizes", "bi-fire", "#e64a19",
             "Detecção de cicatrizes de queimadas e análise de risco de fogo.",
             "Monitoramento via satélite de cicatrizes de queimadas e avaliação do impacto sobre a vegetação.",
             "Dr. Felipe Rocha", 4),
            ("Água e Superfícies Hídricas", "bi-tsunami", "#039be5",
             "Variação de corpos d'água, reservatórios e cheias.",
             "Análise multi-temporal de lagos, rios e reservatórios para apoiar políticas de recursos hídricos.",
             "Dra. Juliana Castro", 5),
            ("Transparência e Dados", "bi-shield-check", "#6a1b9a",
             "Acesso aberto a dados, métodos e códigos de processamento.",
             "Promoção de ciência aberta, com dados e métodos publicados sob licenças livres.",
             "Dr. Marcos Vieira", 6),
            ("Ordenamento Territorial", "bi-map", "#bf6f2a",
             "Suporte técnico a planos diretores e zoneamento.",
             "Apoio técnico a processos de planejamento urbano e zoneamento ambiental nos estados e municípios.",
             "Dra. Renata Borges", 7),
        ]
        for titulo, icone, cor, curta, desc, coord, ordem in grupos:
            GrupoTrabalho.objects.update_or_create(
                titulo=titulo,
                defaults=dict(
                    slug=None,  # será gerado
                    icone=icone, cor=cor, descricao_curta=curta,
                    descricao=desc, coordenador=coord, ordem=ordem, ativo=True,
                ),
            )

        # ---- Tipos de Publicação --------------------------------------- #
        tipos = [
            ("Relatório", "bi-file-earmark-text", "#0d3b66", 1),
            ("Nota Técnica", "bi-file-earmark-medical", "#0277bd", 2),
            ("Artigo", "bi-journal-text", "#1d4e89", 3),
            ("Legislação", "bi-book", "#6a1b9a", 4),
            ("Boletim", "bi-newspaper", "#e64a19", 5),
            ("Manual", "bi-book-half", "#2e7d32", 6),
        ]
        for nome, icone, cor, ordem in tipos:
            TipoPublicacao.objects.update_or_create(
                nome=nome,
                defaults=dict(icone=icone, cor=cor, ordem=ordem),
            )

        # ---- Publicações ------------------------------------------------ #
        pubs = [
            ("Atlas da Cobertura da Terra no Brasil (2010–2023)",
             "Atlas consolidado com mapas temáticos e estatísticas por município, estado e bacia.",
             "MapBiomas; Coleção 9", date(2024, 7, 1), "Relatório", True),
            ("Panorama das Queimadas no Pantanal em 2024",
             "Análise de cicatrizes, severidade e relação com variáveis climáticas.",
             "GT Fogo e Cicatrizes", date(2024, 10, 12), "Nota Técnica", True),
            ("Mudanças Climáticas e Recursos Hídricos na Amazônia",
             "Cenários projeções de vazão e estresse hídrico até 2050.",
             "GT Recursos Hídricos; INPE", date(2024, 5, 8), "Artigo", False),
            ("Guia de Uso de Dados MapBiomas",
             "Como citar, baixar e cruzar os dados da plataforma em pesquisas e políticas públicas.",
             "GT Transparência e Dados", date(2024, 3, 20), "Manual", False),
            ("Boletim Mensal de Fogo nº 42",
             "Resumo mensal de cicatrizes e focos de calor detectados no Brasil.",
             "GT Fogo e Cicatrizes", date(2024, 9, 1), "Boletim", False),
            ("Lei nº 13.089/2015 — Estatuto da Metrópole",
             "Texto consolidado do Estatuto da Metrópole, base legal do planejamento metropolitano.",
             "Presidência da República", date(2015, 1, 12), "Legislação", False),
            ("Nota Técnica: APPs Urbanas em Manaus",
             "Proposição técnica para delimitação de APPs urbanas e áreas consolidadas.",
             "GT Ordenamento Territorial", date(2023, 11, 5), "Nota Técnica", False),
        ]
        for titulo, resumo, autores, pub, tipo_nome, destaque in pubs:
            tipo = TipoPublicacao.objects.get(nome=tipo_nome)
            Publicacao.objects.update_or_create(
                titulo=titulo,
                defaults=dict(
                    resumo=resumo, autores=autores, publicado_em=pub,
                    tipo=tipo, destaque=destaque, ativo=True,
                ),
            )

        # ---- Categorias de notícia -------------------------------------- #
        cats = [
            ("Cobertura e Uso", "#1d4e89"),
            ("Água", "#0277bd"),
            ("Fogo", "#e64a19"),
            ("Clima", "#6a1b9a"),
            ("Eventos", "#f9a825"),
            ("Institucional", "#0d3b66"),
        ]
        for nome, cor in cats:
            CategoriaNoticia.objects.update_or_create(
                nome=nome, defaults=dict(cor=cor)
            )

        # ---- Notícias ---------------------------------------------------- #
        noticias = [
            (
                "MapBiomas lança Coleção 9",
                "Novos dados mostram a evolução do uso da terra no Brasil em 39 anos.",
                ("A Coleção 9 do MapBiomas traz mapas anuais de cobertura e uso da terra "
                 "de 1985 a 2023, com novos módulos de fogo e água, além de estatísticas "
                 "por município, estado e bacia hidrográfica."),
                date(2026, 8, 10), True, "Cobertura e Uso",
            ),
            (
                "Perda de água no Pantanal",
                "Estudo aponta redução drástica na superfície de água no bioma.",
                ("Análise da Coleção 9 revela queda significativa na superfície de água "
                 "no Pantanal nos últimos cinco anos, com impactos diretos sobre a fauna "
                 "e a pesca artesanal."),
                date(2026, 7, 25), True, "Água",
            ),
            (
                "Crescimento da Agricultura",
                "Análise revela que área agrícola dobrou em duas décadas.",
                ("O mapeamento mostra que a área ocupada por agricultura dobrou entre "
                 "2000 e 2023, com expansão concentrada no Matopiba."),
                date(2026, 6, 15), False, "Cobertura e Uso",
            ),
            (
                "Fogo na Amazônia em 2024",
                "Boletim especial analisa cicatrizes de queimadas.",
                ("O módulo de fogo do MapBiomas traz dados inéditos sobre cicatrizes "
                 "de queimadas e sua relação com o desmatamento."),
                date(2026, 5, 4), False, "Fogo",
            ),
            (
                "Seminário Internacional MapBiomas",
                "Encontro reúne especialistas em monitoramento territorial.",
                ("Pesquisadores de mais de 20 países discutem métodos de mapeamento "
                 "colaborativo e ciência aberta."),
                date(2026, 4, 18), False, "Eventos",
            ),
            (
                "Mata Atlântica: fragmentos conectados",
                "Análise identifica corredores ecológicos prioritários.",
                ("Estudo do MapBiomas mapeia os principais fragmentos e corredores da "
                 "Mata Atlântica, apoiando políticas de restauração."),
                date(2026, 3, 22), False, "Cobertura e Uso",
            ),
            (
                "Nova diretoria assume para o biênio 2026–2028",
                "Posse da nova coordenação marca início de novo ciclo de atividades.",
                ("Cerimônia de posse apresenta prioridades do plano de trabalho para o biênio."),
                date(2026, 2, 10), False, "Institucional",
            ),
        ]
        for titulo, resumo, conteudo, pub, destaque, cat_nome in noticias:
            cat, _ = CategoriaNoticia.objects.get_or_create(nome=cat_nome)
            Noticia.objects.update_or_create(
                titulo=titulo,
                defaults=dict(
                    resumo=resumo, conteudo=conteudo,
                    publicado_em=datetime.combine(pub, datetime.min.time(), tzinfo=timezone.utc),
                    destaque=destaque, ativo=True, categoria=cat,
                ),
            )

        # ---- FAQ --------------------------------------------------------- #
        faqs = [
            ("Geral", "O que é o MapBiomas?",
             "O MapBiomas é uma iniciativa multi-institucional que envolve universidades, "
             "ONGs e empresas de tecnologia, dedicada a gerar mapas anuais de cobertura e "
             "uso da terra do Brasil."),
            ("Geral", "Os dados são gratuitos?",
             "Sim, todos os dados, mapas e estatísticas são públicos e gratuitos, sob "
             "licença Creative Commons CC-BY-SA."),
            ("Geral", "Qual a resolução das imagens?",
             "Utilizamos imagens do satélite Landsat (30 metros de resolução espacial) "
             "com classificação pixel a pixel."),
            ("Técnico", "Como os mapas são gerados?",
             "Por meio de algoritmos de aprendizado de máquina aplicados a séries "
             "temporais de imagens Landsat, validados por especialistas."),
            ("Técnico", "Posso usar os dados em publicações?",
             "Sim, basta citar a fonte: Projeto MapBiomas — Coleção X, ano, URL de acesso."),
            ("Técnico", "Com que frequência os mapas são atualizados?",
             "Anualmente. A cada nova coleção, publicamos mapas, estatísticas e painéis."),
            ("Acesso", "Preciso me cadastrar para baixar?",
             "Não, o acesso é totalmente livre."),
            ("Acesso", "Como citar o MapBiomas?",
             "Projeto MapBiomas — Coleção X [ano]. Disponível em: https://mapbiomas.org. "
             "Acesso em: [data]."),
        ]
        for ordem, (cat, q, a) in enumerate(faqs):
            Faq.objects.update_or_create(
                pergunta=q,
                defaults=dict(categoria=cat, resposta=a, ordem=ordem, ativo=True),
            )

        # ---- Glossário --------------------------------------------------- #
        termos = [
            ("Bioma", "Conjunto de ecossistemas com características semelhantes. Ex: Amazônia, Cerrado."),
            ("Antrópico", "Relativo à intervenção humana; áreas modificadas como agricultura e pastagem."),
            ("Landsat", "Programa de satélites de observação da Terra da NASA/USGS."),
            ("Pixel", "Menor elemento de uma imagem raster; cada pixel é classificado em uma classe."),
            ("Cobertura da terra", "O que recobre fisicamente o solo: floresta, água, pasto etc."),
            ("Uso da terra", "A finalidade dada ao território: conservação, agricultura, urbano…"),
            ("Desmatamento", "Remoção da cobertura vegetal nativa, detectada por sensoriamento remoto."),
            ("Queimada", "Incêndio florestal, identificado por cicatriz pós-fogo."),
            ("Mosaico", "Classe que combina agricultura e pastagem em escala fina."),
            ("Mata Ciliar", "Vegetação que margeia rios e corpos d'água."),
            ("Reserva Legal", "Porcentagem da propriedade rural destinada à preservação nativa."),
            ("APP", "Área de Preservação Permanente, protegida por lei."),
            ("Bacia Hidrográfica", "Conjunto de terras drenadas por um rio principal e seus afluentes."),
            ("Cicatriz de Queimada", "Área afetada por fogo, identificada em imagens de satélite."),
        ]
        for termo, defs in termos:
            TermoGlossario.objects.update_or_create(
                termo=termo,
                defaults=dict(definicao=defs, ativo=True),
            )

        # ---- Pilares ----------------------------------------------------- #
        pilares = [
            ("Ciência Colaborativa", "🔬",
             "Rede aberta de pesquisadores e instituições que produzem dados e métodos com rigor científico.", 0),
            ("Tecnologia e Inovação em Nuvem", "💻",
             "Processamento de milhões de imagens de satélite em plataformas escaláveis de cloud computing.", 1),
            ("Transparência e Dados Abertos", "🔓",
             "Publicação aberta, gratuita e com licença livre de mapas, estatísticas e códigos.", 2),
            ("Impacto para Políticas Públicas", "📜",
             "Subsídio a decisões de gestores, pesquisadores, jornalistas e sociedade civil.", 3),
        ]
        for titulo, icone, desc, ordem in pilares:
            Pilar.objects.update_or_create(
                titulo=titulo,
                defaults=dict(icone=icone, descricao=desc, ordem=ordem, ativo=True),
            )

        # ---- Membros ---------------------------------------------------- #
        membros = [
            ("Dra. Ana Souza", "Coordenadora GT Recursos Hídricos", "UFAM"),
            ("Dr. Carlos Lima", "Coordenador GT Mudanças Climáticas", "INPA"),
            ("Dra. Beatriz Alves", "Coordenadora GT Cobertura e Uso", "USP"),
            ("Dr. Felipe Rocha", "Coordenador GT Fogo e Cicatrizes", "UFRJ"),
            ("Dra. Juliana Castro", "Coordenadora GT Água", "UFPA"),
            ("Dr. Marcos Vieira", "Coordenador GT Transparência e Dados", "UFMG"),
            ("Dra. Renata Borges", "Coordenadora GT Ordenamento Territorial", "UFBA"),
        ]
        for ordem, (nome, funcao, inst) in enumerate(membros):
            Membro.objects.update_or_create(
                nome=nome,
                defaults=dict(funcao=funcao, instituicao=inst, ordem=ordem, ativo=True),
            )

        # ---- Parceiros --------------------------------------------------- #
        parceiros = [
            ("Universidade A", "universidade", "https://example.org"),
            ("Instituto B", "ONG", "https://example.org"),
            ("Empresa C", "tecnologia", "https://example.org"),
            ("Rede D", "rede", "https://example.org"),
            ("Fundação E", "fundação", "https://example.org"),
            ("Empresa F", "tecnologia", "https://example.org"),
        ]
        for ordem, (nome, tipo, site) in enumerate(parceiros):
            Parceiro.objects.update_or_create(
                nome=nome,
                defaults=dict(tipo=tipo, site=site, ordem=ordem, ativo=True),
            )

        # ---- Mensagem de teste (só se não houver nenhuma) -------------- #
        if MensagemContato.objects.count() == 0:
            MensagemContato.objects.create(
                nome="Visitante",
                email="visitante@example.org",
                assunto="Interesse em parceria",
                mensagem="Gostaríamos de conversar sobre uma possível parceria.",
            )

        self.stdout.write(self.style.SUCCESS("✅ Dados de demonstração prontos."))
        self.stdout.write(
            "Crie um superusuário com: python manage.py createsuperuser"
        )
