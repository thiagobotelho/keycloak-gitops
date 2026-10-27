# Operação de credenciais e importação do realm

A reconciliação contínua do realm não deve redefinir senhas de usuários. Use bootstrap/initial-passwords.json somente como referência para inicialização controlada; ele não é consumido pelo Kustomize.

Após provisionar o realm e o Secret de usuários, execute:

```bash
python3 scripts/initialize-lab-passwords.py
# Para inicializar somente contas sem credencial password:
python3 scripts/initialize-lab-passwords.py --initialize-missing
```

O script preserva senhas existentes e valida TLS. Confira suas proteções de contexto antes de usar. Reimporte seeds apenas quando desejar inicializar ou recuperar contas específicas. A CA pública do importador deve acompanhar a cadeia TLS do issuer.

Para SAML do Zabbix, mantenha groups como um atributo com múltiplos valores. Ajustes de scopes devem se limitar ao client correspondente, sem alterar scopes globais de outros serviços. Para o console OpenShift, consulte o guia de OIDC no repositório argocd-gitops.
