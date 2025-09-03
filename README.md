# keycloak-gitops

Repositório GitOps para o gerenciamento automatizado do Red Hat Build of Keycloak (RHBK) em cluster OpenShift local (CRC) com Argo CD.

## 📦 Estrutura de Ambientes

Este repositório adota o padrão `kustomize` para separação de ambientes:

```
keycloak-gitops/
├── base/
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── operator.yaml
│   ├── postgresql.yaml
│   ├── keycloak.yaml
│   └── servicemonitor.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── uat/
    │   └── kustomization.yaml
    └── prd/
        └── kustomization.yaml
```

## ⚙️ Componentes

- **Argo CD**: Realiza o deploy contínuo dos manifests declarativos versionados neste repositório.
- **Tekton**: Responsável pelo build da imagem do Keycloak.
- **Kustomize**: Usado para gerenciamento de configurações por ambiente (`dev`, `uat`, `prd`).
- **PostgreSQL**: Banco de dados backend da instância Keycloak.
- **Secrets TLS e banco**: Gerenciados via manifests GitOps.

## 🚀 Fluxo de Deploy

1. O Argo CD monitora os diretórios `overlays/*`.
2. Ao detectar uma alteração, aplica os recursos correspondentes.
3. Cada ambiente possui seu namespace e configurações dedicadas.

## ✅ Pré-requisitos

- OpenShift Local (CRC)
- Git instalado e autenticado
- Argo CD instalado e configurado
- Tekton instalado para build de imagens

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
