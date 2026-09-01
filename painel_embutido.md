

# 📊 Manual: Configuração de Dashboards Públicos no Superset

Este guia abrange as camadas de configuração de arquivos, rede (proxy), permissões de banco de dados e segurança (RBAC).

## 1. Configuração do Superset (`superset_config.py`)

No seu arquivo de configuração (mapeado no Docker), adicione ou ajuste as seguintes diretivas para permitir o acesso anônimo e a integração via Iframe.

```python
# --- ACESSO ANÔNIMO ---
AUTH_ROLE_PUBLIC = 'Public'
PUBLIC_ROLE_LIKE = "Gamma"  # Herda permissões de visualização básicas

# --- SEGURANÇA E IFRAME ---
ENABLE_PROXY_FIX = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True  # Obrigatório se usar HTTPS
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["https://observatorio.provaconceito.tech"]
}

# --- FEATURE FLAGS ---
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_RBAC": True  # Controle de acesso por Dashboard
}

# --- CSP (Content Security Policy) ---
TALISMAN_CONFIG = {
    "content_security_policy": {
        "frame-ancestors": [
            "observatorio.provaconceito.tech",
            "*.provaconceito.tech",
            "self"
        ]
    },
    "force_https": True,
}

# --- REMOÇÃO DE CABEÇALHOS RESTRITIVOS ---
HTTP_HEADERS = {}
OVERRIDE_HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL",
    "Content-Security-Policy": "frame-ancestors 'self' https://observatorio.provaconceito.tech https://*.provaconceito.tech"
}
```

---

## 2. Ajuste no Proxy (Nginx Proxy Manager)

Para evitar o erro **400 Bad Request** causado pelo tamanho excessivo dos cabeçalhos de permissão do Superset, ajuste o Host no NPM:

1. Acesse o painel do **Nginx Proxy Manager**.
2. Edite o Host do Superset (`painel.provaconceito.tech`).
3. Vá na aba **Advanced** e cole as seguintes diretivas:

```nginx
# Aumenta os buffers para aceitar URLs e Headers gigantes (Resolve Erro 400)
large_client_header_buffers 4 32k;
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;

# Timeouts para queries longas
proxy_read_timeout 300;
proxy_connect_timeout 300;
proxy_send_timeout 300;

# Informa ao Superset o protocolo original
proxy_set_header X-Forwarded-Proto $scheme;
```

---

## 3. Concessão de Permissões via CLI (Bypass de Interface)

Caso a interface de "Roles" esteja lenta ou inacessível, utilize o terminal para garantir que o papel `Public` tenha acesso aos dados.

### Para dar acesso total (Apenas Testes - Perigoso):
```bash
docker exec -it app_superset superset shell
# Dentro do shell:
from superset import db, security_manager
role = security_manager.find_role("Public")
perm = security_manager.find_permission_view_menu("all_datasource_access", "all_datasource_access")
security_manager.add_permission_role(role, perm)
db.session.commit()
exit()
```

### Para remover acesso total e manter segurança:
```python
# Dentro do superset shell:
security_manager.del_permission_role(role, perm)
db.session.commit()
```

---

## 4. Segurança e Refinamento (Modo Produção)

Para garantir que o público veja apenas o que é autorizado:

### A. Atribuição de Role ao Dashboard
1. Vá em **Dashboards** -> **Edit Properties**.
2. No campo **Roles**, adicione o papel **Public**.
3. Isso garante que o Dashboard específico seja visível para anônimos (RBAC).

### B. Acesso Mínimo ao Dataset
1. Vá em **Security** -> **List Roles** -> **Edit Public**.
2. Remova `all_datasource_access`.
3. Adicione apenas o dataset específico: `datasource access on [Nome_do_Banco].[Nome_da_Tabela]`.

### C. Sincronização Final
Sempre que alterar permissões ou o arquivo `superset_config.py`, reinicie e sincronize:
```bash
docker compose restart superset
docker exec -it app_superset superset init
```

---

## 5. Implementação do Iframe

Para embutir o dashboard no site `observatorio.provaconceito.tech`, utilize a URL de **Permalink** gerada pelo Superset com o parâmetro `standalone`:

```html
<iframe
  src="https://painel.provaconceito.tech/superset/dashboard/p/ID_DO_DASHBOARD/?standalone=true"
  width="100%"
  height="800px"
  frameborder="0"
></iframe>
```

**Benefícios desta configuração:**
- **Invisibilidade:** O usuário anônimo não vê menus, barras de busca ou SQL Lab.
- **Isolamento:** Somente domínios autorizados no `frame-ancestors` podem exibir o painel.
- **Performance:** Buffers de proxy ajustados para evitar quedas em carregamentos pesados.