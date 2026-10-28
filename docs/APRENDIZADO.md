# Clients e identidade


Client OIDC exige client_id, callback exato, scopes, audience e política de acesso; o segredo é provisionado fora do Git. Client SAML exige entityID, ACS e mapeamento de atributos. Grupos autenticados não atribuem privilégios automaticamente: confira o mapeamento de roles da aplicação. Teste callback incorreto, usuário sem grupo e token expirado.

## Separar autenticação e autorização

O realm publica identidade e grupos. OpenShift RBAC, Argo CD RBAC, Grafana e Zabbix atribuem seus próprios privilégios. Consulte o procedimento do consumidor para validar um usuário autorizado e outro sem grupo. Certificado SAML, CA HTTPS e certificado mTLS do Istio têm finalidades e ciclos de renovação distintos.
