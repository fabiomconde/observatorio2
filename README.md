# 🌎 MapBiomas Clone

Clone institucional do site do MapBiomas, construído em **Django 5**.

> O objetivo é servir como projeto de estudo / portfólio, replicando as
> principais seções de um site institucional de monitoramento territorial:
> home com destaques, quem-somos, biomas, coleções, notícias (com busca,
> filtro e paginação), FAQ, glossário com navegação por letra e contato.

---

## ✨ Funcionalidades

- 🏠 Home com hero, estatísticas, coleção em destaque, notícias, biomas e parceiros
- 📰 Notícias com busca, filtro por categoria, paginação e página de detalhe
- 🌳 Listagem e detalhe de **Biomas** (Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa, Pantanal)
- 📦 Listagem de **Coleções** anuais (com destaque)
- ❓ **FAQ** agrupado por categoria, em accordion
- 📚 **Glossário** com navegação A–Z
- ✉️ **Contato** com persistência das mensagens no banco (visíveis no admin)
- 🔐 **Django Admin** completo para todos os modelos
- 🌱 Comando `seed_data` que popula o banco com dados de demonstração (idempotente)
- 🐳 Docker + docker-compose (Postgres + Django + Gunicorn)
- 🎨 Tema verde inspirado na identidade visual do projeto
- 🌐 PT-BR, timezone America/Sao_Paulo

---

## 🚀 Como rodar

### Opção 1 — Local (SQLite, mais simples)

```bash
# 1. Instale dependências
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Migrações + dados de demonstração
python manage.py migrate
python manage.py seed_data

# 3. Crie um superusuário para acessar /admin
python manage.py createsuperuser

# 4. Suba o servidor
python manage.py runserver
```

Acesse:
- Site: http://localhost:8000/
- Admin: http://localhost:8000/admin/

### Opção 2 — Docker (Postgres + Gunicorn)

```bash
cp .env.example .env
docker compose up -d --build
docker compose logs -f web
```

Acesse http://localhost:8000/

---

## 🗂 Estrutura

```
mapbiomas_clone/
├── config/                  # Projeto Django (settings, urls, wsgi, asgi)
├── core/                    # App principal
│   ├── models.py            # Bioma, Colecao, Noticia, Faq, TermoGlossario, …
│   ├── views.py             # Views públicas
│   ├── urls.py
│   ├── admin.py
│   ├── context_processors.py
│   ├── management/commands/
│   │   └── seed_data.py     # Popula o banco com dados demo
│   ├── migrations/
│   ├── templates/core/      # Templates do site
│   └── static/core/         # CSS/JS/img
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## 🧩 Principais modelos

| Modelo | Descrição |
|---|---|
| `Bioma` | Biomas brasileiros monitorados (com cor e ícone) |
| `Colecao` | Coleções anuais de mapas (com ano inicial/final e destaque) |
| `CategoriaNoticia` | Categorias para as notícias |
| `Noticia` | Notícias com slug, resumo, conteúdo, imagem e data |
| `Faq` | Perguntas frequentes, agrupadas por categoria |
| `TermoGlossario` | Termos do glossário |
| `Pilar` | Pilares do projeto (Ciência, Tecnologia, …) |
| `Parceiro` | Parceiros institucionais |
| `MensagemContato` | Mensagens enviadas pelo formulário público |

---

## 🛠 Comandos úteis (via Makefile)

```bash
make install        # instala dependências
make migrate        # aplica migrações
make makemigrations # cria novas migrações
make seed           # popula dados de demonstração
make superuser      # cria superusuário
make run            # sobe o servidor dev
make test           # roda os testes
make docker-up      # sobe docker-compose
make docker-down    # derruba docker-compose
make docker-logs    # tail dos logs
make clean          # remove caches e db sqlite
```

---

## 📝 Licença

Projeto de estudo, sem fins comerciais. Dados abertos sob CC-BY-SA.
