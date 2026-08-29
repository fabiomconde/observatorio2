"""
Idempotent seed command — populates the database with Observatório Socioambiental-flavored
demo data so the project is browsable on a fresh install.
"""

from datetime import date, datetime, timezone

from django.core.management.base import BaseCommand

from core.models import (
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

        # ---- Regiões ----------------------------------------------------- #
        regioes_data = [
            ("Alto Madeira", "Região localizada no setor oeste do município, reunindo distritos próximos às divisas com o Acre.", "bi-tree", "#2e7d32"),
            ("Médio Madeira", "Região que concentra a sede municipal e importantes áreas de ocupação e circulação ao longo da BR-364.", "bi-building", "#0d3b66"),
            ("Baixo Madeira", "Região caracterizada principalmente pelo acesso fluvial e pelas comunidades localizadas ao longo do Rio Madeira.", "bi-water", "#0277bd"),
        ]
        regioes_dict = {}
        for nome, desc, icone, cor in regioes_data:
            reg, _ = Regiao.objects.update_or_create(
                nome=nome,
                defaults=dict(descricao=desc, icone=icone, cor=cor, ativo=True),
            )
            regioes_dict[nome] = reg

        # ---- Distritos --------------------------------------------------- #
        distritos_data = [
            {
                "nome": "Porto Velho",
                "codigo_ibge": "110020505",
                "tipo": "Distrito-Sede",
                "populacao": 412807,
                "domicilios": 136420,
                "area_km2": 9234,
                "densidade": 44.70,
                "regiao": "Médio Madeira",
                "criacao": "1914",
                "distancia_sede_km": 0,
                "descricao": "Concentra a maior parte da população urbana e da infraestrutura da capital, incluindo o centro administrativo, comercial e de serviços.",
                "tags": ["sede municipal", "urbano", "serviços", "administração", "infraestrutura"],
                "icone": "bi-building-fill",
                "cor": "#0d3b66",
            },
            {
                "nome": "Jaci-Paraná",
                "codigo_ibge": "110020520",
                "tipo": "Distrito",
                "populacao": 11672,
                "domicilios": 3927,
                "area_km2": 6457,
                "densidade": 1.81,
                "regiao": "Médio Madeira",
                "criacao": "Antes de 1945",
                "distancia_sede_km": 90,
                "descricao": "Segundo distrito mais populoso, localizado ao longo da BR-364. A economia baseia-se na agricultura familiar e pecuária.",
                "tags": ["BR-364", "agricultura familiar", "pecuária", "serviços públicos", "infraestrutura"],
                "icone": "bi-truck",
                "cor": "#1d4e89",
            },
            {
                "nome": "Vista Alegre do Abunã",
                "codigo_ibge": "110020545",
                "tipo": "Distrito",
                "populacao": 8260,
                "domicilios": 2578,
                "area_km2": 1493,
                "densidade": 5.53,
                "regiao": "Alto Madeira",
                "criacao": "22 de dezembro de 1981",
                "distancia_sede_km": None,
                "descricao": "Localizado na região do Alto Madeira, próximo à divisa com o Acre. Integra o conjunto de localidades beneficiadas pelos serviços da UPA de Jaci-Paraná.",
                "tags": ["Alto Madeira", "divisa com Acre", "serviços de saúde"],
                "icone": "bi-geo-alt-fill",
                "cor": "#2e7d32",
            },
            {
                "nome": "Mutum-Paraná",
                "codigo_ibge": "110020525",
                "tipo": "Distrito",
                "populacao": 7509,
                "domicilios": 2567,
                "area_km2": 3573,
                "densidade": 2.10,
                "regiao": "Médio Madeira",
                "criacao": "11 de dezembro de 1985",
                "distancia_sede_km": None,
                "descricao": "Conhecido também como Nova Mutum-Paraná. A população foi relocada para um novo projeto urbanístico após parte da antiga localidade ser submersa pelo reservatório da Usina Hidrelétrica de Jirau.",
                "tags": ["Nova Mutum-Paraná", "UHE Jirau", "reassentamento", "BR-364", "infraestrutura"],
                "icone": "bi-lightning-charge-fill",
                "cor": "#e64a19",
            },
            {
                "nome": "Extrema",
                "codigo_ibge": "110020517",
                "tipo": "Distrito",
                "populacao": 7171,
                "domicilios": 2304,
                "area_km2": 2022,
                "densidade": 3.55,
                "regiao": "Alto Madeira",
                "criacao": "5 de janeiro de 1998",
                "distancia_sede_km": 194,
                "descricao": "Localizado na divisa com o Acre e a Bolívia. Faz parte do grupo de distritos relacionado ao processo de emancipação para formação do município de Extrema.",
                "tags": ["Alto Madeira", "divisa", "emancipação", "território"],
                "icone": "bi-flag-fill",
                "cor": "#388e3c",
            },
            {
                "nome": "Nova Califórnia",
                "codigo_ibge": "110020535",
                "tipo": "Distrito",
                "populacao": 5216,
                "domicilios": 1649,
                "area_km2": 732,
                "densidade": 7.12,
                "regiao": "Alto Madeira",
                "criacao": "21 de novembro de 1985",
                "distancia_sede_km": None,
                "descricao": "Localizado no Alto Madeira, faz parte do grupo de distritos que pleiteiam emancipação para formar o município de Extrema. A economia baseia-se na agricultura e pecuária familiar.",
                "tags": ["Alto Madeira", "agricultura familiar", "pecuária", "emancipação"],
                "icone": "bi-flower1",
                "cor": "#4caf50",
            },
            {
                "nome": "Abunã",
                "codigo_ibge": "110020510",
                "tipo": "Distrito",
                "populacao": 2385,
                "domicilios": 789,
                "area_km2": 1597,
                "densidade": 1.49,
                "regiao": "Médio Madeira",
                "criacao": "21 de setembro de 1943",
                "distancia_sede_km": None,
                "descricao": "Um dos distritos mais antigos, localizado ao longo da BR-364. Integra a região do Médio Madeira e é beneficiado por serviços da UPA de Jaci-Paraná.",
                "tags": ["BR-364", "Médio Madeira", "saúde", "história territorial"],
                "icone": "bi-signpost-fill",
                "cor": "#1565c0",
            },
            {
                "nome": "Calama",
                "codigo_ibge": "110020515",
                "tipo": "Distrito",
                "populacao": 2312,
                "domicilios": 678,
                "area_km2": 2908,
                "densidade": 0.79,
                "regiao": "Baixo Madeira",
                "criacao": "Antes de 1944",
                "distancia_sede_km": 128,
                "descricao": "Localizado na foz do Rio Ji-Paraná, é o último povoado de Rondônia no curso de descida do Rio Madeira. O acesso é predominantemente fluvial.",
                "tags": ["Baixo Madeira", "acesso fluvial", "Rio Madeira", "Rio Ji-Paraná", "áreas de interesse ambiental"],
                "icone": "bi-water",
                "cor": "#0277bd",
            },
            {
                "nome": "São Carlos",
                "codigo_ibge": "110020540",
                "tipo": "Distrito",
                "populacao": 1176,
                "domicilios": 379,
                "area_km2": 1274,
                "densidade": None,
                "regiao": "Baixo Madeira",
                "criacao": "21 de novembro de 1985",
                "distancia_sede_km": None,
                "descricao": "Distrito do Baixo Madeira que reúne localidades como Lago do Cuniã, Terra Caída, Araçá, Periquitos e Santa Luzia.",
                "tags": ["Baixo Madeira", "Lago do Cuniã", "comunidades", "socioambiental"],
                "icone": "bi-tsunami",
                "cor": "#0288d1",
            },
            {
                "nome": "Demarcação",
                "codigo_ibge": "110020516",
                "tipo": "Distrito",
                "populacao": 845,
                "domicilios": 248,
                "area_km2": 3389,
                "densidade": 0.25,
                "regiao": "Baixo Madeira",
                "criacao": "26 de junho de 1997",
                "distancia_sede_km": 175,
                "descricao": "Um dos distritos menos populosos, localizado no Baixo Madeira, com acesso predominantemente fluvial.",
                "tags": ["Baixo Madeira", "acesso fluvial", "socioambiental"],
                "icone": "bi-compass-fill",
                "cor": "#0097a7",
            },
            {
                "nome": "Nazaré",
                "codigo_ibge": "110020530",
                "tipo": "Distrito",
                "populacao": 607,
                "domicilios": 198,
                "area_km2": None,
                "densidade": None,
                "regiao": "Baixo Madeira",
                "criacao": "26 de junho de 1997",
                "distancia_sede_km": 119,
                "descricao": "Menor distrito em população, localizado no Baixo Madeira. Possui as localidades de Araçatuba e Boa Vitória.",
                "tags": ["Baixo Madeira", "acesso fluvial", "comunidades", "socioambiental"],
                "icone": "bi-life-preserver",
                "cor": "#00acc1",
            },
            {
                "nome": "Fortaleza do Abunã",
                "codigo_ibge": "110020518",
                "tipo": "Distrito",
                "populacao": 474,
                "domicilios": 168,
                "area_km2": 1274,
                "densidade": 0.37,
                "regiao": "Alto Madeira",
                "criacao": "21 de novembro de 1985",
                "distancia_sede_km": None,
                "descricao": "Segundo menor distrito em população, localizado no Alto Madeira próximo à divisa com o Acre. Faz parte do grupo de distritos relacionado ao processo de emancipação para formação do município de Extrema.",
                "tags": ["Alto Madeira", "divisa com Acre", "emancipação", "território"],
                "icone": "bi-shield-shaded",
                "cor": "#2e7d32",
            },
        ]
        for item in distritos_data:
            reg = regioes_dict.get(item["regiao"])
            Distrito.objects.update_or_create(
                nome=item["nome"],
                defaults=dict(
                    codigo_ibge=item["codigo_ibge"],
                    tipo=item["tipo"],
                    populacao=item["populacao"],
                    domicilios=item["domicilios"],
                    area_km2=item["area_km2"],
                    densidade=item["densidade"],
                    regiao=reg,
                    criacao=item["criacao"],
                    distancia_sede_km=item["distancia_sede_km"],
                    descricao=item["descricao"],
                    tags=item["tags"],
                    icone=item["icone"],
                    cor=item["cor"],
                    ativo=True,
                ),
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
        # grupos = [
        #     ("Recursos Hídricos", "bi-droplet-half", "#0277bd",
        #      "Análise de bacias, qualidade da água e disponibilidade hídrica no território.",
        #      "Monitoramento de bacias hidrográficas, qualidade da água e disponibilidade para abastecimento, "
        #      "irrigação e geração de energia.",
        #      "Dra. Ana Souza", 1),
        #     ("Mudanças Climáticas", "bi-cloud-rain", "#1d4e89",
        #      "Riscos climáticos, emissões e adaptação nos biomas brasileiros.",
        #      "Estudo de cenários climáticos, emissões de GEE e estratégias de adaptação em nível regional.",
        #      "Dr. Carlos Lima", 2),
        #     ("Cobertura e Uso da Terra", "bi-globe-americas", "#2e7d32",
        #      "Mapeamento anual da cobertura vegetal e uso do solo desde 1985.",
        #      "Geração dos mapas anuais de cobertura e uso da terra, em parceria com universidades e ONGs.",
        #      "Dra. Beatriz Alves", 3),
        #     ("Fogo e Cicatrizes", "bi-fire", "#e64a19",
        #      "Detecção de cicatrizes de queimadas e análise de risco de fogo.",
        #      "Monitoramento via satélite de cicatrizes de queimadas e avaliação do impacto sobre a vegetação.",
        #      "Dr. Felipe Rocha", 4),
        #     ("Água e Superfícies Hídricas", "bi-tsunami", "#039be5",
        #      "Variação de corpos d'água, reservatórios e cheias.",
        #      "Análise multi-temporal de lagos, rios e reservatórios para apoiar políticas de recursos hídricos.",
        #      "Dra. Juliana Castro", 5),
        #     ("Transparência e Dados", "bi-shield-check", "#6a1b9a",
        #      "Acesso aberto a dados, métodos e códigos de processamento.",
        #      "Promoção de ciência aberta, com dados e métodos publicados sob licenças livres.",
        #      "Dr. Marcos Vieira", 6),
        #     ("Ordenamento Territorial", "bi-map", "#bf6f2a",
        #      "Suporte técnico a planos diretores e zoneamento.",
        #      "Apoio técnico a processos de planejamento urbano e zoneamento ambiental nos estados e municípios.",
        #      "Dra. Renata Borges", 7),
        # ]
        grupos = [

    ("Conflitos Agrários, Fundiários e Territoriais", "bi-map", "#795548",

     "Monitoramento dos conflitos relacionados à terra, ao território e à regularização fundiária.",

     "Acompanhamento de disputas por terra e território, ocupações, despejos, processos de grilagem "
     "e regularização fundiária, identificando comunidades e territórios afetados.",

     "Coordenação do Eixo", 1),

    ("Pressões Ambientais, Mudanças Climáticas e Justiça Climática", "bi-globe-americas", "#2e7d32",

     "Monitoramento das pressões sobre o meio ambiente e dos impactos das mudanças climáticas.",

     "Análise de desmatamento, queimadas, degradação ambiental, eventos climáticos extremos, "
     "disponibilidade e qualidade da água, contaminação e desigualdades relacionadas à justiça climática.",

     "Coordenação do Eixo", 2),

    ("Violências, Segurança Pública e Direitos Humanos", "bi-shield-exclamation", "#c62828",

     "Acompanhamento das diferentes formas de violência e das violações de direitos nos territórios.",

     "Monitoramento de ameaças, agressões, homicídios, criminalização, violência institucional e "
     "situações de risco enfrentadas por comunidades, defensores de direitos e outros grupos vulnerabilizados.",

     "Coordenação do Eixo", 3),

    ("Dinâmicas Econômicas, Produtivas e Conflitos Socioambientais", "bi-bar-chart-line", "#ef6c00",

     "Análise das atividades econômicas e produtivas e de seus impactos sobre os territórios.",

     "Estudo das relações entre agropecuária, mineração, exploração florestal, infraestrutura, "
     "empreendimentos, cadeias produtivas e a geração ou agravamento de conflitos socioambientais.",

     "Coordenação do Eixo", 4),

    ("Respostas Institucionais e Políticas Públicas", "bi-building-check", "#1565c0",

     "Análise da atuação do Estado diante dos conflitos e das demandas das comunidades.",

     "Monitoramento da presença ou ausência do Estado, das ações de prevenção, proteção e reparação, "
     "bem como das políticas públicas e iniciativas voltadas à garantia de direitos nos territórios em conflito.",

     "Coordenação do Eixo", 5),

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
             "Observatório Socioambiental; Coleção 9", date(2024, 7, 1), "Relatório", True),
            ("Panorama das Queimadas no Pantanal em 2024",
             "Análise de cicatrizes, severidade e relação com variáveis climáticas.",
             "GT Fogo e Cicatrizes", date(2024, 10, 12), "Nota Técnica", True),
            ("Mudanças Climáticas e Recursos Hídricos na Amazônia",
             "Cenários projeções de vazão e estresse hídrico até 2050.",
             "GT Recursos Hídricos; INPE", date(2024, 5, 8), "Artigo", False),
            ("Guia de Uso de Dados Observatório Socioambiental",
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
                "Observatório Socioambiental lança Coleção 9",
                "Novos dados mostram a evolução do uso da terra no Brasil em 39 anos.",
                ("A Coleção 9 do Observatório Socioambiental traz mapas anuais de cobertura e uso da terra "
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
                ("O módulo de fogo do Observatório Socioambiental traz dados inéditos sobre cicatrizes "
                 "de queimadas e sua relação com o desmatamento."),
                date(2026, 5, 4), False, "Fogo",
            ),
            (
                "Seminário Internacional Observatório Socioambiental",
                "Encontro reúne especialistas em monitoramento territorial.",
                ("Pesquisadores de mais de 20 países discutem métodos de mapeamento "
                 "colaborativo e ciência aberta."),
                date(2026, 4, 18), False, "Eventos",
            ),
            (
                "Mata Atlântica: fragmentos conectados",
                "Análise identifica corredores ecológicos prioritários.",
                ("Estudo do Observatório Socioambiental mapeia os principais fragmentos e corredores da "
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
            ("Geral", "O que é o Observatório Socioambiental?",
             "O Observatório Socioambiental é uma iniciativa multi-institucional que envolve universidades, "
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
             "Sim, basta citar a fonte: Projeto Observatório Socioambiental — Coleção X, ano, URL de acesso."),
            ("Técnico", "Com que frequência os mapas são atualizados?",
             "Anualmente. A cada nova coleção, publicamos mapas, estatísticas e painéis."),
            ("Acesso", "Preciso me cadastrar para baixar?",
             "Não, o acesso é totalmente livre."),
            ("Acesso", "Como citar o Observatório Socioambiental?",
             "Projeto Observatório Socioambiental — Coleção X [ano]. Disponível em: https://mapbiomas.org. "
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
    ("Conflitos Socioambientais e Direitos Humanos", "⚖️",
     "Centralidade dos conflitos socioambientais e da garantia dos direitos humanos na compreensão da realidade territorial.", 0),

    ("Justiça Climática e Equidade", "🌎",
     "Análise da justiça climática, do racismo ambiental e das desigualdades que afetam de forma diferente comunidades e territórios.", 1),

    ("Territorialidade e Integração", "🗺️",
     "Leitura integrada do território, considerando as relações entre sociedade, ambiente, economia, cultura e espaço.", 2),

    ("Conhecimento e Evidências", "🔬",
     "Produção de conhecimento baseada em evidências, métodos transparentes e informações rastreáveis e confiáveis.", 3),

    ("Interdisciplinaridade e Colaboração", "🤝",
     "Integração de diferentes áreas do conhecimento, saberes e experiências para compreender problemas complexos de forma colaborativa.", 4),

    ("Transparência, Ética e Responsabilidade", "🔎",
     "Gestão responsável da informação, com transparência, ética, proteção de dados e compromisso com a qualidade das informações.", 5),

    ("Incidência e Transformação Social", "📢",
     "Produção de conhecimento voltada à participação social, às políticas públicas e à transformação das realidades e desigualdades identificadas.", 6),
]
        for titulo, icone, desc, ordem in pilares:
            Pilar.objects.update_or_create(
                titulo=titulo,
                defaults=dict(icone=icone, descricao=desc, ordem=ordem, ativo=True),
            )

        # ---- Membros ---------------------------------------------------- #
        # membros = [
        #     ("Dra. Ana Souza", "Coordenadora GT Recursos Hídricos", "UFAM"),
        #     ("Dr. Carlos Lima", "Coordenador GT Mudanças Climáticas", "INPA"),
        #     ("Dra. Beatriz Alves", "Coordenadora GT Cobertura e Uso", "USP"),
        #     ("Dr. Felipe Rocha", "Coordenador GT Fogo e Cicatrizes", "UFRJ"),
        #     ("Dra. Juliana Castro", "Coordenadora GT Água", "UFPA"),
        #     ("Dr. Marcos Vieira", "Coordenador GT Transparência e Dados", "UFMG"),
        #     ("Dra. Renata Borges", "Coordenadora GT Ordenamento Territorial", "UFBA"),
        # ]

        membros = [
            ("Amanda", "Coordenadora Adjunta", "UNIR"),
            ("Larissa", "Equipe de Dados — Dados Sociais e Direitos Humanos", "UNIR"),
            ("Laura", "Equipe de Dados — Dados Ambientais, Econômicos e Produtivos", "UNIR"),
            ("Fábio", "Coordenador da Plataforma Digital", "IFRO"),
            ("Júnior", "Apoio à Plataforma Digital", "UNIR"),
            ("Maria Eduarda", "Bolsista de Comunicação", "UNIR"),
            ("Berg/Talita", "Apoio Administrativo", "UNIR"),
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
