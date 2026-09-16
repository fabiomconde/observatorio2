# Revisão de UX, responsividade e iconografia

Esta revisão foi criada como uma camada incremental sobre a interface existente do Observatório. O objetivo não é substituir a identidade visual do projeto, mas melhorar a experiência de navegação e consulta de dados preservando a paleta institucional verde + dourado já definida em `site.css`.

## Mudanças implementadas

- navegação mobile convertida de menu expandido vertical para drawer/offcanvas;
- manutenção da identidade visual verde e dourada na home;
- ajuste da escala tipográfica do hero em telas pequenas;
- área de acesso rápido a dashboards, mapa territorial, distritos e coleções;
- cards de acesso rápido com rolagem horizontal e `scroll-snap` no celular;
- contadores da home obtidos do banco, evitando números fixos no template;
- revisão dos cards de pilares com iconografia semântica;
- modal dos dashboards refeito para desktop e celular, incluindo barra de contexto, estado de carregamento, botão para nova aba, Escape e devolução de foco;
- melhorias de foco visível, áreas de toque e suporte a `prefers-reduced-motion`;
- restauração dos emojis específicos de biomas quando eles carregam significado próprio.

## Iconografia

Os SVGs semânticos usados nos pilares foram adaptados do **Tabler Icons**, biblioteca open source sob licença MIT. A seleção foi feita pelo significado de cada pilar, e não por um ícone genérico:

| Pilar | SVG escolhido |
| --- | --- |
| Conflitos Socioambientais e Direitos Humanos | `scale` |
| Justiça Climática e Equidade | `sun-wind` |
| Territorialidade e Integração | `map-2` |
| Conhecimento e Evidências | `book-2` |
| Interdisciplinaridade e Colaboração | `network` |
| Transparência, Ética e Responsabilidade | `eye-check` |
| Incidência e Transformação Social | `speakerphone` |

Fonte: https://github.com/tabler/tabler-icons

Licença: MIT — Copyright (c) 2020-2026 Paweł Kuna.

## Decisões de UX

### Identidade antes de ornamentação

A cor azul utilizada no primeiro protótipo foi removida. A revisão utiliza as variáveis já existentes (`--cor-principal`, `--cor-escura`, `--cor-destaque`) para evitar a criação de uma segunda identidade visual dentro do mesmo produto.

### Mobile como layout próprio

No primeiro protótipo, o menu apenas empilhava o conteúdo do desktop. Na revisão, a navegação passa a usar um drawer lateral. Isso reduz a altura consumida pelo menu, mantém o contexto da página e melhora a área útil em telas de 360–430 px.

### Significado antes de consistência artificial

Emojis que representam entidades específicas não são removidos automaticamente. A substituição por SVG é aplicada onde existe um mapeamento semântico claro, especialmente nos pilares institucionais.

### Dados sem números fixos

Os indicadores da home passam a refletir o conteúdo ativo cadastrado no banco: distritos, eixos, publicações e dashboards.

## Checklist de teste manual

Testar pelo menos nas larguras de 360, 390, 768, 1024 e 1440 px:

1. abrir/fechar o menu mobile e seus dropdowns;
2. verificar se busca e contato continuam acessíveis dentro do drawer;
3. validar hero e barra de indicadores sem overflow horizontal;
4. deslizar os cards de acesso rápido no celular;
5. abrir a página "O Projeto" e conferir os sete SVGs dos pilares;
6. abrir um dashboard no desktop e no celular;
7. fechar o dashboard por botão, clique no fundo e tecla Escape;
8. navegar por teclado verificando foco visível;
9. confirmar que os emojis de biomas continuam sendo exibidos onde cadastrados.
