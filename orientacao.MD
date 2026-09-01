
# Guia Completo de Gráficos do Apache Superset

## Índice por Categoria

1. [Correlation (Correlação)](#correlation)
2. [Distribution (Distribuição)](#distribution)
3. [Evolution (Evolução)](#evolution)
4. [Flow (Fluxo)](#flow)
5. [KPI (Indicadores)](#kpi)
6. [Map (Mapas)](#map)
7. [Part of a Whole (Partes de um Todo)](#part-of-a-whole)
8. [Ranking (Ranking)](#ranking)
9. [Table (Tabelas)](#table)
10. [Outros Gráficos](#outros)

---

## CORRELATION

### 1. Heatmap
**Objetivo:** Visualizar a intensidade da relação entre duas variáveis categóricas através de cores.

**Exemplo de dados (Vendas por Mês e Região):**

| | Jan | Fev | Mar | Abr | Mai |
|---|-----|-----|-----|-----|-----|
| **Norte** | 8.200 | 7.500 | 9.100 | 8.800 | 10.200 |
| **Nordeste** | 12.400 | 11.800 | 14.200 | 13.500 | 15.600 |
| **Sudeste** | 28.500 | 26.900 | 31.200 | 29.800 | 34.100 |

**Configuração no Superset:**
- **DIMENSIONS:** `Região`, `Mês` (ou colunas de linha e coluna)
- **METRICS:** `SUM(Vendas)`
- **SORT BY:** Valor (para ordenar)

### 2. Scatter Plot
**Objetivo:** Analisar a correlação entre duas variáveis numéricas.

**Exemplo de dados (Preço vs. Volume de Vendas):**

| Produto | Preço (R$) | Volume Vendido | Margem (%) |
|---------|------------|----------------|------------|
| Produto A | 99,90 | 850 | 35% |
| Produto B | 149,90 | 420 | 42% |
| Produto C | 199,90 | 310 | 48% |

**Configuração no Superset:**
- **X-AXIS:** `Preço`
- **Y-AXIS:** `Volume Vendido`
- **SERIES / COLOR:** `Produto`
- **SIZE:** `Margem` (opcional para bolhas)

### 3. Bubble Chart
**Objetivo:** Adicionar uma terceira dimensão (tamanho da bolha) à relação entre duas variáveis.

**Configuração no Superset:**
- **X-AXIS:** `Preço`
- **Y-AXIS:** `Volume Vendido`
- **SERIES:** `Produto`
- **SIZE:** `Margem`
- **BUBBLE SIZE:** Escolher o campo para definir o tamanho

### 4. Bubble Chart (legacy)
**Objetivo:** Versão anterior do gráfico de bolhas com diferentes opções de customização.

### 5. Parallel Coordinates
**Objetivo:** Visualizar múltiplas variáveis numéricas simultaneamente para encontrar padrões.

**Exemplo de dados (Comparação de Produtos):**

| Produto | Preço | Volume | Margem | Satisfação |
|---------|-------|--------|--------|------------|
| Produto A | 99,90 | 850 | 35% | 4,5 |
| Produto B | 149,90 | 420 | 42% | 4,2 |
| Produto C | 199,90 | 310 | 48% | 4,8 |

**Configuração no Superset:**
- **DIMENSIONS:** `Produto` (para cor)
- **METRICS:** Todas as variáveis numéricas

---

## DISTRIBUTION

### 6. Box Plot
**Objetivo:** Mostrar distribuição estatística incluindo mediana, quartis e outliers.

**Exemplo de dados (Salários por Departamento):**

| Departamento | Mínimo | Q1 | Mediana | Q3 | Máximo |
|--------------|--------|-----|---------|-----|---------|
| Vendas | 2.500 | 3.800 | 5.200 | 7.500 | 15.000 |
| TI | 4.000 | 6.000 | 8.500 | 12.000 | 20.000 |
| Marketing | 3.000 | 4.500 | 6.000 | 8.200 | 14.000 |

**Configuração no Superset:**
- **DIMENSIONS:** `Departamento`
- **METRICS:** `Salário`
- **DISTRIBUTION:** Configurar para Box Plot

### 7. Histogram
**Objetivo:** Visualizar a frequência de valores em intervalos (bins).

**Exemplo de dados (Faixa Etária dos Clientes):**

| Faixa Etária | Qtd. Clientes | % Total |
|--------------|---------------|---------|
| 18-25 | 2.340 | 18% |
| 26-35 | 4.550 | 35% |
| 36-45 | 3.120 | 24% |
| 46-60 | 2.080 | 16% |

**Configuração no Superset:**
- **METRICS:** `Idade` (com contagem)
- **BINS:** Definir número de intervalos
- **DIMENSIONS:** Deixar em branco

### 8. Word Cloud
**Objetivo:** Destacar termos mais frequentes em textos.

**Exemplo de dados (Termos de Pesquisa):**

| Termo | Frequência |
|-------|------------|
| Superset | 1.250 |
| Dashboard | 980 |
| Analytics | 750 |
| SQL | 620 |

**Configuração no Superset:**
- **DIMENSIONS:** `Termo`
- **METRICS:** `Frequência`
- **MAX NUMBER OF WORDS:** Limite de palavras

### 9. Calendar
**Objetivo:** Visualizar dados em um formato de calendário.

**Exemplo de dados (Vendas Diárias):**

| Data | Vendas |
|------|--------|
| 01/05/2026 | 2.300 |
| 02/05/2026 | 1.800 |
| 03/05/2026 | 2.500 |

**Configuração no Superset:**
- **TIME COLUMN:** `Data`
- **METRICS:** `SUM(Vendas)`
- **TIME GRAIN:** `Day`

---

## EVOLUTION

### 10. Area Chart
**Objetivo:** Mostrar volumes acumulados e mudanças de proporção ao longo do tempo.

**Exemplo de dados (Participação por Canal):**

| Mês | Mobile (%) | Desktop (%) | Tablet (%) |
|-----|------------|-------------|------------|
| Jan/2026 | 45% | 35% | 20% |
| Fev/2026 | 48% | 33% | 19% |
| Mar/2026 | 52% | 30% | 18% |

**Configuração no Superset:**
- **TIME COLUMN:** `Mês`
- **TIME GRAIN:** `Month`
- **METRICS:** `AVG(Mobile)`, `AVG(Desktop)`, `AVG(Tablet)`

### 11. Bar Chart (Evolução Temporal)
**Objetivo:** Visualizar dados discretos ao longo do tempo.

**Exemplo de dados (Novos Usuários por Semana):**

| Semana | Usuários | Conversões |
|--------|----------|------------|
| Semana 1 | 1.250 | 175 |
| Semana 2 | 1.380 | 193 |
| Semana 3 | 1.120 | 157 |

**Configuração no Superset:**
- **TIME COLUMN:** `Semana`
- **TIME GRAIN:** `Week`
- **METRICS:** `SUM(Usuários)`, `SUM(Conversões)`

### 12. Line Chart
**Objetivo:** Visualizar tendências contínuas ao longo do tempo.

**Exemplo de dados (Vendas Mensais):**

| Mês | Receita (R$) | Nº Pedidos |
|-----|-------------|------------|
| Jan/2026 | 52.300 | 1.045 |
| Fev/2026 | 48.700 | 974 |
| Mar/2026 | 61.200 | 1.224 |

**Configuração no Superset:**
- **TIME COLUMN:** `Mês`
- **TIME GRAIN:** `Month`
- **METRICS:** `SUM(Receita)`, `SUM(Nº Pedidos)`

### 13. Smooth Line
**Objetivo:** Suavizar flutuações para identificar tendências de longo prazo.

**Configuração:** Mesma do Line Chart, com opção de suavização.

### 14. Stepped Line
**Objetivo:** Enfatizar mudanças abruptas entre intervalos.

**Configuração:** Mesma do Line Chart, com estilo stepped.

### 15. Time-series Percent Change
**Objetivo:** Mostrar a variação percentual ao longo do tempo.

**Configuração no Superset:**
- **TIME COLUMN:** Data
- **METRICS:** Escolher métrica
- **PERIOD:** Comparação período a período

### 16. Time-series Period Pivot
**Objetivo:** Visualizar dados temporais em formato pivotado.

### 17. Time-series Table
**Objetivo:** Tabela com dados temporais e totais.

**Exemplo de dados (Vendas Mensais com Totais):**

| Mês | Receita | Cresc. % |
|-----|---------|----------|
| Jan/2026 | 52.300 | - |
| Fev/2026 | 48.700 | -6,9% |
| Mar/2026 | 61.200 | +25,7% |

### 18. Horizon Chart
**Objetivo:** Visualizar séries temporais múltiplas em espaço reduzido.

---

## FLOW

### 19. Sankey Chart
**Objetivo:** Visualizar fluxos entre estágios de um processo.

**Exemplo de dados (Funil de Conversão):**

| Origem | Destino | Volume |
|--------|---------|--------|
| Visitantes | Leads | 8.750 |
| Leads | Oportunidades | 3.500 |
| Oportunidades | Propostas | 1.750 |
| Propostas | Fechados | 875 |

**Configuração no Superset:**
- **DIMENSIONS:** `Origem`, `Destino`
- **METRICS:** `SUM(Volume)`

### 20. Chord Diagram
**Objetivo:** Visualizar relações entre grupos com fluxos.

**Configuração no Superset:**
- **SOURCE:** Grupo de origem
- **TARGET:** Grupo de destino
- **VALUE:** Valor do fluxo

### 21. Funnel Chart
**Objetivo:** Visualizar perda progressiva em um funil de conversão.

**Exemplo de dados (Funil de Marketing):**

| Estágio | Qtd. | Taxa Conv. |
|---------|------|------------|
| Visitantes | 50.000 | 100% |
| Leads | 8.750 | 17,5% |
| Oportunidades | 3.500 | 40% |

**Configuração no Superset:**
- **DIMENSIONS:** `Estágio`
- **METRICS:** `SUM(Qtd)`

### 22. Gantt Chart
**Objetivo:** Visualizar cronogramas e dependências entre tarefas.

**Exemplo de dados (Projeto):**

| Tarefa | Início | Fim | Duração |
|--------|--------|-----|---------|
| Planejamento | 01/05 | 10/05 | 10 |
| Desenvolvimento | 11/05 | 20/05 | 10 |
| Testes | 21/05 | 25/05 | 5 |

**Configuração no Superset:**
- **DIMENSIONS:** `Tarefa`
- **START:** Data início
- **END:** Data fim
- **DURATION:** Duração

---

## KPI

### 23. Big Number
**Objetivo:** Destacar um único indicador proeminente.

**Exemplo de dados (KPI Geral):**

| Métrica | Valor | Meta | Var. (%) |
|---------|-------|------|----------|
| Receita Total | R$ 2.847.500 | R$ 2.800.000 | +1,7% |

**Configuração no Superset:**
- **METRICS:** `SUM(Receita)`
- **TIME COLUMN:** Período base
- **COMPARE TO:** Período anterior

### 24. Gauge Chart
**Objetivo:** Mostrar progresso em direção a uma meta.

**Exemplo de dados (Progresso):**

| Métrica | Valor | Meta | % Meta |
|---------|-------|------|---------|
| Vendas | 2.847.500 | 3.000.000 | 94,9% |

**Configuração no Superset:**
- **METRICS:** `SUM(Vendas)`
- **MIN:** Valor mínimo (0)
- **MAX:** Meta (3.000.000)

### 25. Bulletin Chart
**Objetivo:** Mostrar KPIs com contexto e visualização adicional.

### 26. Big Number Total
**Objetivo:** Destacar valor total com comparação.

---

## MAP

### 27. Country Map
**Objetivo:** Dados agregados por país.

**Exemplo de dados (Vendas por País):**

| País | Vendas (R$) | Clientes |
|------|-------------|----------|
| Brasil | 156.300 | 3.126 |
| EUA | 423.500 | 7.060 |
| Alemanha | 189.200 | 3.152 |

**Configuração no Superset:**
- **COUNTRY COLUMN:** `País`
- **METRICS:** `SUM(Vendas)`

### 28. World Map
**Objetivo:** Visualização global de dados por país ou região.

### 29. MapBox
**Objetivo:** Mapas interativos com alta customização.

### 30. Cartodagram
**Objetivo:** Mapas com dados de movimento e trajetória.

### 31. deck.gl (Arc, Path, 3D Hexagon, etc.)
**Objetivo:** Visualizações geoespaciais avançadas com WebGL.

**Tipos disponíveis:**
- **decks.gl Arc:** Arcos entre pontos
- **deck.gl Path:** Rotas e trajetórias
- **deck.gl 3D Hexagon:** Hexágonos 3D em mapa
- **deck.gl Contour:** Contornos geográficos
- **deck.gl Geojson:** Dados Geojson
- **deck.gl Grid:** Grade em mapa
- **deck.gl Heatmap:** Mapa de calor geoespacial

**Configuração no Superset:**
- **LATITUDE COLUMN:** Latitude
- **LONGITUDE COLUMN:** Longitude
- **METRICS:** Valor a ser plotado
- **LAYER OPTIONS:** Configurações específicas

---

## PART OF A WHOLE

### 32. Pie Chart
**Objetivo:** Mostrar a composição percentual de um todo.

**Exemplo de dados (Receita por Produto):**

| Produto | Receita (R$) | % |
|---------|--------------|---|
| Produto A | 45.200 | 28% |
| Produto B | 38.700 | 24% |
| Produto C | 32.100 | 20% |

**Configuração no Superset:**
- **DIMENSIONS:** `Produto`
- **METRICS:** `SUM(Receita)`

### 33. Donut Chart
**Objetivo:** Mesmo do Pie, com espaço vazio no centro.

**Configuração:** Igual ao Pie Chart, com estilo Donut.

### 34. Treemap
**Objetivo:** Hierarquias com proporções visuais.

**Exemplo de dados (Vendas por Categoria e Subcategoria):**

| Categoria | Subcategoria | Vendas |
|-----------|--------------|--------|
| Eletrônicos | Smartphones | 45.200 |
| Eletrônicos | Notebooks | 38.700 |
| Roupas | Camisetas | 32.100 |

**Configuração no Superset:**
- **DIMENSIONS:** `Categoria`, `Subcategoria`
- **METRICS:** `SUM(Vendas)`

### 35. Sunburst Chart
**Objetivo:** Hierarquias aninhadas com vários níveis.

**Configuração:** Múltiplas dimensões hierárquicas.

### 36. Partition Chart
**Objetivo:** Visualizar proporções em forma de partição.

### 37. Nightingale Rose Chart
**Objetivo:** Diagrama de rosa com proporções.

### 38. Waterfall Chart
**Objetivo:** Mostrar composição cumulativa positiva e negativa.

**Exemplo de dados (Resultado Financeiro):**

| Item | Valor | Tipo |
|------|-------|------|
| Receita Bruta | 100.000 | Início |
| Impostos | -25.000 | Negativo |
| Custos | -30.000 | Negativo |
| Lucro Líquido | 45.000 | Fim |

**Configuração no Superset:**
- **DIMENSIONS:** `Item`
- **METRICS:** `SUM(Valor)`
- **TYPE:** Positivo/Negativo

---

## RANKING

### 39. Bar Chart (Categórico)
**Objetivo:** Comparar valores entre categorias distintas.

**Exemplo de dados (Desempenho por Canal):**

| Canal | Visitas | Conversões | ROI (%) |
|-------|---------|------------|---------|
| Google Ads | 12.500 | 625 | 400% |
| Orgânico | 15.300 | 918 | — |
| E-mail | 3.100 | 248 | 620% |

**Configuração no Superset:**
- **X-AXIS:** `Canal`
- **METRICS:** `SUM(Visitas)`, `SUM(Conversões)`

### 40. Horizontal Bar Chart
**Objetivo:** Quando os nomes das categorias são longos.

**Configuração:** Igual ao Bar Chart, orientação horizontal.

### 41. Radar Chart
**Objetivo:** Comparar múltiplas métricas para diferentes entidades.

**Exemplo de dados (Produto Performance):**

| Produto | Qualidade | Preço | Design | Suporte |
|---------|-----------|-------|--------|---------|
| Produto A | 4.5 | 3.2 | 4.0 | 4.8 |
| Produto B | 4.0 | 4.5 | 3.5 | 3.8 |
| Produto C | 3.8 | 3.8 | 4.8 | 4.2 |

**Configuração no Superset:**
- **DIMENSIONS:** `Produto`
- **METRICS:** `Qualidade`, `Preço`, `Design`, `Suporte`

### 42. Paired t-test Table
**Objetivo:** Comparar duas amostras pareadas estatisticamente.

---

## TABLE

### 43. Pivot Table
**Objetivo:** Análise multidimensional com totais e agregações.

**Exemplo de dados (Receita por Região e Canal):**

| Região \ Canal | Google | Facebook | Total |
|----------------|--------|----------|-------|
| **Norte** | 12.300 | 8.100 | 35.600 |
| **Nordeste** | 18.700 | 11.200 | 52.300 |
| **Total** | **87.900** | **57.400** | **249.100** |

**Configuração no Superset:**
- **ROWS:** `Região`
- **COLUMNS:** `Canal`
- **METRICS:** `SUM(Receita)`

### 44. Time-series Table
**Objetivo:** Tabela com dados temporais e totais.

### 45. Table
**Objetivo:** Visualização tabular simples com cores condicionais.

**Exemplo de dados:**

| Produto | Vendas | Meta | Status |
|---------|--------|------|--------|
| A | 45.200 | 40.000 | ✅ |
| B | 38.700 | 45.000 | ❌ |
| C | 32.100 | 30.000 | ✅ |

**Configuração no Superset:**
- **DIMENSIONS:** Colunas a serem exibidas
- **METRICS:** Métricas calculadas
- **COLOR:** Configurar cores condicionais

---

## OUTROS

### 46. Mixed Chart
**Objetivo:** Combinar diferentes tipos de gráfico em um só.

**Exemplo de dados (Receita vs. Margem):**

| Mês | Receita (R$) | Margem (%) |
|-----|--------------|------------|
| Jan | 52.300 | 28% |
| Fev | 48.700 | 30% |
| Mar | 61.200 | 26% |

**Configuração no Superset:**
- **TIME COLUMN:** `Mês`
- **METRICS (Bar):** `SUM(Receita)`
- **METRICS (Line):** `AVG(Margem)`

### 47. Tree Chart
**Objetivo:** Visualizar hierarquias organizacionais.

**Exemplo de dados (Estrutura Organizacional):**

| Pai | Filho | Nível |
|-----|-------|-------|
| CEO | VP Vendas | 1 |
| VP Vendas | Gerente Norte | 2 |
| VP Vendas | Gerente Sul | 2 |

**Configuração no Superset:**
- **DIMENSIONS:** Hierarquia de colunas

### 48. Graph Chart
**Objetivo:** Visualizar redes e conexões.

### 49. Generic Chart
**Objetivo:** Gráfico customizado com opções avançadas.

### 50. Handlebars
**Objetivo:** Visualização personalizada com Handlebars templates.

### 51. Tags
**Objetivo:** Exibir tags e categorias.

---

## Glossário de Configurações

| Termo | Descrição |
|-------|-----------|
| **TIME COLUMN** | Coluna com datas para séries temporais |
| **TIME GRAIN** | Nível de agregação (Hora, Dia, Mês, Ano) |
| **DIMENSIONS** | Campo categórico para agrupar dados |
| **METRICS** | Valor numérico com agregação (SUM, AVG, COUNT, etc.) |
| **GROUP BY** | Agrupar por dimensão |
| **FILTER** | Condições para filtrar dados |
| **SORT BY** | Ordenar por campo específico |
| **LIMIT** | Número máximo de resultados |

---