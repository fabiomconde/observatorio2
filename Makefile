PYTHON ?= python3
MANAGE = $(PYTHON) manage.py

.PHONY: help install migrate makemigrations seed superuser run test lint clean docker-up docker-down docker-logs

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - instala dependências"
	@echo "  make migrate       - aplica migrações"
	@echo "  make makemigrations- cria novas migrações"
	@echo "  make seed          - popula o banco com dados de demonstração"
	@echo "  make superuser     - cria um superusuário"
	@echo "  make run           - sobe o servidor de desenvolvimento"
	@echo "  make test          - roda os testes"
	@echo "  make docker-up     - sobe containers (Postgres + Django)"
	@echo "  make docker-down   - derruba containers"
	@echo "  make docker-logs   - mostra logs do web"

install:
	$(PYTHON) -m pip install -r requirements.txt

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

seed:
	$(MANAGE) seed_data

superuser:
	$(MANAGE) createsuperuser

run:
	$(MANAGE) runserver 0.0.0.0:8000

test:
	$(MANAGE) test

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f web

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf staticfiles db.sqlite3
