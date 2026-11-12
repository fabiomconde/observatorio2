#!/usr/bin/env python3
"""Generate detailed documentation for Django admin models.
Each model gets a Markdown file under `docs/administracao/` with:
- Overview with URLs
- Table placeholder for fields
- Step‑by‑step CRUD sections
- Image placeholders (list & form)
"""
import os

# List of (Title, slug) for all admin models
models = [
    ("Bioma", "bioma"),
    ("Categoria de notícia", "categorianoticia"),
    ("Coleção", "colecao"),
    ("Dashboard", "dashboard"),
    ("Distrito", "distrito"),
    ("Divulgação Popular", "publicacaoredesocial"),
    ("Eixo Temático", "grupotrabalho"),
    ("Membro", "membro"),
    ("Mensagem de contato", "mensagemcontato"),
    ("Notícia", "noticia"),
    ("Parceiro", "parceiro"),
    ("FAQ", "faq"),
    ("Pilar", "pilar"),
    ("Publicação", "publicacao"),
    ("Região", "regiao"),
    ("Termo do glossário", "termoglossario"),
    ("Tipo de publicação", "tipopublicacao"),
]

out_dir = "docs/administracao"
os.makedirs(out_dir, exist_ok=True)
# Directory for shared images used by all manuals
images_dir = "docs/imagens"
os.makedirs(images_dir, exist_ok=True)
print(f"📂 images directory prepared: {images_dir}")
template = """# {title} – Cadastro no Django Admin

> **Objetivo**: Descrever passo a passo como criar, editar e excluir registros do modelo **{title}** dentro da interface de administração do Observatório.

## Visão geral
- Listagem: http://dev0:8000/admin/core/{slug}/
- Adicionar novo: http://dev0:8000/admin/core/{slug}/add/

## Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| _campo_ | _tipo_ | _descrição_ |

## Operações CRUD
### Criar
1. Clique em **Adicionar {title}**.
2. Preencha os campos necessários.
3. Clique em **Salvar**.

### Editar
1. Na lista, clique no registro que deseja editar.
2. Modifique os campos.
3. Clique em **Salvar**.

### Excluir
1. Selecione o registro na lista.
2. Escolha **Excluir** no menu de ações.
3. Confirme a exclusão.

## Capturas de tela
![Listagem {title}](../imagens/{slug}_list.png)
![Formulário {title}](../imagens/{slug}_form.png)
"""

for title, slug in models:
    path = os.path.join(out_dir, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(template.format(title=title, slug=slug))
    print(f"✅ criada: {path}")
    # create placeholder image files for this model
    open(os.path.join(images_dir, f"{slug}_list.png"), "a").close()
    open(os.path.join(images_dir, f"{slug}_form.png"), "a").close()

