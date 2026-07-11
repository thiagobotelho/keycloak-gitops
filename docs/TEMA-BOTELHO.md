# Tema Botelho Identity

O `keycloak-gitops` consome o tema como artefato versionado:

```text
docker/themes/rhbk-theme-botelho-1.2.5.jar
```

O Dockerfile copia esse JAR para `/opt/keycloak/providers/` e executa
`kc.sh build`, conforme o modelo de distribuição de temas por archive/JAR do
Keycloak.

Fonte do tema: <https://github.com/thiagobotelho/keycloak-theme-botelho>

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
- rollback fica claro: trocar `rhbk-theme-botelho-1.2.5.jar` por outra versão.

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
2. Gerar versão nova, por exemplo `1.2.5`.
3. Publicar release com:
   - `rhbk-theme-botelho-1.2.5.jar`;
   - checksum SHA256;
   - screenshots/preview.
4. Atualizar `keycloak-gitops/docker/Dockerfile` para copiar o JAR novo.
5. Atualizar tag da imagem customizada do Keycloak.
6. Sincronizar `keycloak-dev` no Argo CD.

## Melhorias implementadas no 1.2.5

- Remove a borda/faixa superior remanescente do cartão de login com CSS
  específico e override runtime após o carregamento do PatternFly.
- Suaviza o foco dos campos e harmoniza o botão de visibilidade de senha com o
  restante do input.
- Renomeia assets CSS/JS para reduzir cache visual antigo após rollout.
- Melhora a apresentação das ações nativas do Keycloak: recuperação de senha,
  cadastro quando habilitado, lembrar de mim e provedores de identidade.
- Documenta que recursos como “Esqueceu sua senha?” dependem de configuração do
  realm e, para reset real por e-mail, SMTP configurado.
- Mantém compatibilidade com os fluxos nativos do RHBK/Keycloak.

## Aplicação no Keycloak

O realm deve referenciar o tema pelo nome `botelho` nos tipos suportados pelo
archive:

- `login`;
- `admin`.

O tema não força recursos de autenticação. Links como “Esqueceu sua senha?”,
cadastro, lembrar de mim e botões de provedores externos aparecem quando o
próprio realm os habilita. Para recuperação de senha por e-mail, configure SMTP
no realm.

Se o tema for alterado em runtime, reinicie o pod do Keycloak para garantir que
o provider e os caches sejam recarregados.

## Referências oficiais

- Keycloak Themes: <https://www.keycloak.org/ui-customization/themes>
- Keycloak Server Developer Guide: <https://www.keycloak.org/docs/latest/server_development/>
