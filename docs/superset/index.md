# Superset

O Apache Superset é usado para construir gráficos e dashboards consumidos pelo portal.

Fluxo recomendado:

1. disponibilizar o dataset;
2. validar tipos, métricas e dimensões;
3. criar os gráficos;
4. montar e publicar o dashboard;
5. conceder somente as permissões necessárias;
6. incorporar o dashboard no Observatório.

A segurança deve ser resolvida por **RBAC/permissões**. CSS pode melhorar a UX,
mas não é mecanismo de autorização.


## Orientações existentes

- [Guia de gráficos](graficos.md)
- [Guia legado de integração de painéis](painel-embutido-legado.md)

As configurações de permissões e de links do Superset devem ser testadas no ambiente implantado.
