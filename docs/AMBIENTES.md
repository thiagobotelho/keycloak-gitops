# Ambientes

Este repositório usa `base/` e `overlays/{desenvolvimento,aceite,producao}`.

- `desenvolvimento`: namespace `keycloak-dev`, URLs CRC e recursos de laboratório.
- `aceite`: namespace `keycloak-uat`, hosts `.example.invalid` como placeholder obrigatório.
- `producao`: namespace `keycloak-prd`, hosts `.example.invalid` como placeholder obrigatório.

Validação:

```bash
oc kustomize overlays/desenvolvimento >/tmp/keycloak-dev.yaml
oc kustomize overlays/aceite >/tmp/keycloak-aceite.yaml
oc kustomize overlays/producao >/tmp/keycloak-prod.yaml
oc apply --dry-run=client -k overlays/desenvolvimento
```

Secrets obrigatórios:

- `<namespace>/keycloak-db-secret`: `username`, `password`, `database`.
- `<namespace>/keycloak-observability-users`: `GRAFANA_ADMIN_PASSWORD`, `ZABBIX_ADMIN_PASSWORD`, `OBSERVABILITY_ADMIN_PASSWORD`.
- Secret inicial do Operator: `<keycloak-name>-initial-admin`.

Parametrização:

- `KEYCLOAK_URL`, `GRAFANA_BASE_URL` e `ZABBIX_BASE_URL` são injetados por overlay no `keycloak-config-cli`.
- O realm usa `$(env:...)`; não há client secret ou senha real no Git.

Automação preservada:

- `.github/workflows/validate.yml`: renderiza Kustomizations e executa `yamllint`.
- `.github/workflows/build.yml`: mantém build/push da imagem Keycloak customizada.
- `scripts/bootstrap-observability-users.sh`: cria/atualiza Secret de usuários sem imprimir senhas.
