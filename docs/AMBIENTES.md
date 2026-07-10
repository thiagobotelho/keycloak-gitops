# Ambientes

Este repositório usa `base/` e `overlays/{desenvolvimento,aceite,producao}`.

- `desenvolvimento`: namespace `keycloak-dev`, URLs CRC e recursos de laboratório.
- `aceite`: namespace `keycloak-aceite`, hosts `.example.invalid` como placeholder obrigatório.
- `producao`: namespace `keycloak-producao`, hosts `.example.invalid` como placeholder obrigatório.

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
- `PYROSCOPE_APPLICATION_NAME` recebe o mesmo valor de `SERVICE_NAME`, mantendo o nome do serviço igual em traces e profiles.
- `PYROSCOPE_LABELS` é definido por overlay com `service_name`, `service_namespace`, `namespace` e `deployment_environment_name`.
- O realm usa `$(env:...)`; não há client secret ou senha real no Git.

O datasource Tempo do `grafana-gitops` usa esses labels para abrir profiles do
Keycloak a partir de um span. Se renomear namespace, serviço ou ambiente,
atualize também `SERVICE_NAME` e `PYROSCOPE_LABELS`.
