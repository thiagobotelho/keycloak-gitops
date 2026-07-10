# Tema Botelho Identity

O `keycloak-gitops` consome o tema como artefato versionado:

```text
docker/themes/rhbk-theme-botelho-1.2.0.jar
```

O Dockerfile copia esse JAR para `/opt/keycloak/providers/` e executa
`kc.sh build`, conforme o modelo de distribuição de temas por archive/JAR do
Keycloak.

## Recomendação de organização

Mantenha o desenvolvimento do tema em um repositório próprio, por exemplo:

```text
keycloak-theme-botelho
```

Motivos:

- o tema tem fonte, CSS, JS, assets, preview, changelog e build próprios;
- revisar layout por Pull Request fica mais simples;
- o `keycloak-gitops` continua focado no deploy do Keycloak;
- a imagem do Keycloak passa a consumir apenas artefatos versionados e
  publicados;
- rollback fica claro: trocar `rhbk-theme-botelho-1.2.0.jar` por outra versão.

Estrutura recomendada:

```text
keycloak-theme-botelho/
├── src/main/resources/META-INF/keycloak-themes.json
├── src/main/resources/theme/botelho/login/
├── src/main/resources/theme/botelho/admin/
├── preview/
├── scripts/
├── pom.xml
├── README.md
└── CHANGELOG.md
```

## Fluxo recomendado

1. Ajustar CSS/FTL/JS no repo do tema.
2. Gerar versão nova, por exemplo `1.2.1`.
3. Publicar release com:
   - `rhbk-theme-botelho-1.2.1.jar`;
   - checksum SHA256;
   - screenshots/preview.
4. Atualizar `keycloak-gitops/docker/Dockerfile` para copiar o JAR novo.
5. Atualizar tag da imagem customizada do Keycloak.
6. Sincronizar `keycloak-dev` no Argo CD.

## Pontos de melhoria observados no 1.2.0

- Refinar o espaçamento vertical entre logo, linha superior do card e título.
- Ajustar a área inferior de controles para melhorar o seletor de tema em telas
  pequenas.
- Validar contraste e foco visível nos modos claro e escuro.
- Criar screenshots automatizados do login/admin para comparar regressões.
- Adicionar teste de empacotamento conferindo `META-INF/keycloak-themes.json`,
  `theme.properties`, CSS, JS e assets esperados.

## Aplicação no Keycloak

O realm deve referenciar o tema pelo nome `botelho` nos tipos suportados pelo
archive:

- `login`;
- `admin`.

Se o tema for alterado em runtime, reinicie o pod do Keycloak para garantir que
o provider e os caches sejam recarregados.

## Referências oficiais

- Keycloak Themes: <https://www.keycloak.org/ui-customization/themes>
- Keycloak Server Developer Guide: <https://www.keycloak.org/docs/latest/server_development/>
