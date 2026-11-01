# Desenvolvimento

## Django

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DB_ENGINE=sqlite python manage.py migrate
DB_ENGINE=sqlite python manage.py test
DB_ENGINE=sqlite python manage.py runserver
```

## Manual

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Validação:

```bash
DB_ENGINE=sqlite python manage.py check
DB_ENGINE=sqlite python manage.py makemigrations --check --dry-run
DB_ENGINE=sqlite python manage.py test
mkdocs build --strict
```


### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-docs.txt
$env:DB_ENGINE = "sqlite"
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python -m mkdocs build --strict
python -m mkdocs serve
```

Em produção, **não** execute `seed_data` automaticamente: o comando atual
utiliza `update_or_create` para popular dados de demonstração e pode
sobrescrever dados editados. A carga inicial deve ser deliberada e precedida
de backup e avaliação dos dados existentes.
