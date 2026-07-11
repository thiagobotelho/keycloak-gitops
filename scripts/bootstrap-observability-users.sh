#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "${ROOT_DIR}/.env" ]]; then
  # shellcheck disable=SC1091
  set -a; source "${ROOT_DIR}/.env"; set +a
fi

OC_BIN="${OC_BIN:-oc}"
ENVIRONMENT="${ENVIRONMENT:-dev}"
NAMESPACE="${NAMESPACE:-keycloak-${ENVIRONMENT}}"
SECRET_NAME="${KEYCLOAK_OBSERVABILITY_USERS_SECRET:-keycloak-observability-users}"

generate_password() {
  openssl rand -base64 36 | tr -d '\n'
}

existing_key() {
  local key="$1"
  "${OC_BIN}" -n "${NAMESPACE}" get secret "${SECRET_NAME}" \
    -o "jsonpath={.data.${key}}" 2>/dev/null | base64 -d 2>/dev/null || true
}

require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "[ERROR] Comando obrigatório não encontrado: $1" >&2
    exit 1
  }
}

require "${OC_BIN}"
require openssl
require base64

"${OC_BIN}" create namespace "${NAMESPACE}" --dry-run=client -o yaml | "${OC_BIN}" apply --server-side -f - >/dev/null

GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD:-$(existing_key GRAFANA_ADMIN_PASSWORD)}"
ZABBIX_ADMIN_PASSWORD="${ZABBIX_ADMIN_PASSWORD:-$(existing_key ZABBIX_ADMIN_PASSWORD)}"
OBSERVABILITY_ADMIN_PASSWORD="${OBSERVABILITY_ADMIN_PASSWORD:-$(existing_key OBSERVABILITY_ADMIN_PASSWORD)}"

GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD:-$(generate_password)}"
ZABBIX_ADMIN_PASSWORD="${ZABBIX_ADMIN_PASSWORD:-$(generate_password)}"
OBSERVABILITY_ADMIN_PASSWORD="${OBSERVABILITY_ADMIN_PASSWORD:-$(generate_password)}"

"${OC_BIN}" -n "${NAMESPACE}" create secret generic "${SECRET_NAME}" \
  --from-literal=GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD}" \
  --from-literal=ZABBIX_ADMIN_PASSWORD="${ZABBIX_ADMIN_PASSWORD}" \
  --from-literal=OBSERVABILITY_ADMIN_PASSWORD="${OBSERVABILITY_ADMIN_PASSWORD}" \
  --dry-run=client -o yaml | "${OC_BIN}" apply --server-side -f - >/dev/null
"${OC_BIN}" -n "${NAMESPACE}" annotate secret "${SECRET_NAME}" \
  kubectl.kubernetes.io/last-applied-configuration- >/dev/null 2>&1 || true

echo "[OK] Secret ${NAMESPACE}/${SECRET_NAME} reconciliado."
echo "[INFO] Valores sensíveis não foram exibidos. Reexecute para manter os valores existentes ou defina variáveis para rotacionar."
