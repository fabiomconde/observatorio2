# Publicação e acesso público no Superset

Valide este procedimento contra a versão do Superset em execução, porque nomes
de opções e recursos de RBAC podem variar.

## Checklist

1. confirme que o dashboard usa somente datasets que podem ser expostos;
2. marque o dashboard como **Published**;
3. revise o papel usado por visitantes anônimos;
4. conceda acesso somente ao dataset/dashboard necessário;
5. teste em janela anônima;
6. confirme as origens permitidas para iframe.

## Menor privilégio

Evite transformar o papel público em cópia ampla de perfis internos. Dependendo
da versão, o ambiente pode usar acesso por dataset ou RBAC/viewer por dashboard.

## Incorporação

O modo standalone reduz elementos de navegação dentro do iframe. A autorização
continua sendo responsabilidade do Superset.

Sempre teste como visitante anônimo: gráficos, filtros, mobile e tentativas de
acesso a Explore/telas administrativas.


Veja também o [documento legado de incorporação](painel-embutido-legado.md).
As regras antigas de permissões não substituem uma avaliação de segurança.
