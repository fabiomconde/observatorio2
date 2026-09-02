
# 📊 Manual: Configuração de Dashboards Públicos no Superset

Este guia abrange as camadas de configuração de arquivos, rede (proxy), permissões de banco de dados e segurança (RBAC).

## 1. Configuração do Superset (`superset_config.py`)

No seu arquivo de configuração, adicione ou ajuste as seguintes diretivas para permitir o acesso anônimo, integração via Iframe e **segurança avançada**.

```python
# --- ACESSO ANÔNIMO ---
AUTH_ROLE_PUBLIC = 'Public'
PUBLIC_ROLE_LIKE = "Gamma"  # Herda permissões de visualização básicas

# --- SEGURANÇA ---
ENABLE_PROXY_FIX = True
CUSTOM_STACKTRACE = False  # Segurança: não mostra erros de código/logs para o usuário
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True 
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "origins": ["https://observatorio.provaconceito.tech"]
}

# --- FEATURE FLAGS ---
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_RBAC": True,
    "MOBILE_CONSUMPTION_MODE": True # Empilha gráficos automaticamente em telas pequenas
}

# --- CSP (Content Security Policy) ---
TALISMAN_CONFIG = {
    "content_security_policy": {
        "frame-ancestors": ["observatorio.provaconceito.tech", "*.provaconceito.tech", "self"]
    },
    "force_https": True,
}

# --- HEADERS ---
HTTP_HEADERS = {}
OVERRIDE_HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL",
    "Content-Security-Policy": "frame-ancestors 'self' https://observatorio.provaconceito.tech https://*.provaconceito.tech"
}
```

---

## 2. Ajuste no Proxy (Nginx Proxy Manager)

Para evitar o erro **400 Bad Request** e permitir URLs longas de permissões, configure na aba **Advanced** do NPM:

```nginx
large_client_header_buffers 4 32k;
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
proxy_read_timeout 300;
proxy_set_header X-Forwarded-Proto $scheme;
```

---

## 3. Blindagem de Segurança via CLI (Shell)

Para impedir que o usuário público clique nos títulos dos gráficos e seja encaminhado para a área de edição (Explore), execute o script de remoção de permissões:

```bash
docker exec -it app_superset superset shell
```

Dentro do shell, cole o código abaixo:

```python
from superset import db, security_manager
role = security_manager.find_role("Public")

# Lista de permissões que permitem navegar fora do Dashboard
perms_para_remover = [
    ("can_explore", "Superset"),
    ("can_explore_json", "Superset"),
    ("can_share_chart", "Superset"),
    ("can_share_dashboard", "Superset")
]

for p_name, p_view in perms_para_remover:
    perm = security_manager.find_permission_view_menu(p_name, p_view)
    if perm:
        security_manager.del_permission_role(role, perm)

db.session.commit()
print("--- Blindagem aplicada: Usuário público não pode mais explorar gráficos ---")
exit()
```

---

## 4. Estilização e Bloqueio de UI (CSS do Dashboard)

Para garantir que os links nos títulos dos gráficos sejam desativados visualmente, aplique este CSS diretamente no Dashboard:

1. No Dashboard, clique em **Edit Dashboard** -> `...` (Menu) -> **Edit CSS**.
2. Cole o código:

```css
/* Desativa o clique nos títulos dos gráficos para evitar saída do dashboard */
.slice_header .header-title a {
    pointer-events: none;
    cursor: default;
    color: inherit;
    text-decoration: none;
}

/* Esconde o botão de ações (três pontinhos) de cada gráfico */
.slice_header .actions-trigger {
    display: none !important;
}
```

---

## 5. Implementação do Iframe Responsivo

Para alternar entre dashboards Desktop e Mobile no Django, utilize a detecção de User-Agent e o parâmetro `standalone=2` (que remove bordas e títulos extras).

### Template Django:
```html
<iframe
  src="{{ url_dashboard }}&standalone=2"
  width="100%"
  height="100%"
  frameborder="0"
  style="min-height: 80vh;"
></iframe>
```

---

## 6. Sincronização e Manutenção

Sempre que criar um novo dashboard, lembre-se de:
1. Alterar para **Published**.
2. Adicionar o papel **Public** em **Edit Properties** -> **Roles**.
3. Rodar o comando de sincronização:

```bash
docker exec -it app_superset superset init
```

**Resultado:** O dashboard agora é um componente estético e funcional, sem barras de navegação, sem links clicáveis nos títulos e otimizado para dispositivos móveis.