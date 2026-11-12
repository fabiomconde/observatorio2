import os

models = [
    ("Notícia", "noticia"),
    ("Publicação", "publicacao"),
    ("Mensagem de contato", "mensagemcontato"),
    ("Divulgação Popular", "publicacaoredesocial"),
    ("Distrito", "distrito"),
    ("Coleção", "colecao"),
    ("Dashboard", "dashboard"),
    ("Bioma", "bioma"),
    ("Eixo Temático", "grupotrabalho"),
    ("Glossário", "termoglossario"),
    ("FAQ", "faq"),
    ("Membro", "membro"),
    ("Parceiro", "parceiro"),
    ("Usuário", "usuario"),
    ("Grupo", "grupo"),
]

template = """# {title} – Cadastro no Django Admin

> **Objetivo**: Descrever passo a passo como criar, editar e excluir registros do modelo **{name}** dentro da interface de administração do Observatório.

<!-- copie o conteúdo do template acima e cole aqui -->"""

out_dir = "docs/administracao"
os.makedirs(out_dir, exist_ok=True)

for title, name in models:
    path = os.path.join(out_dir, f"{name}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(template.format(title=title, name=name))
    print(f"✅ criada: {path}")
