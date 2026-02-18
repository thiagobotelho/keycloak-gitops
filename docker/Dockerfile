# Etapa de build com Keycloak customizado
FROM registry.redhat.io/rhbk/keycloak-rhel9:26.2 AS builder

# Variáveis de ambiente
ENV KC_DB=postgres \
    KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=true \
    KC_EVENT_METRICS_USER_ENABLED=true \
    KC_FEATURES=opentelemetry \
    KC_TRACING_ENABLED=true \
    KC_TRACING_SAMPLER_TYPE=parentbased_traceidratio

# Copiando os Themes
COPY --chown=keycloak:keycloak --chmod=644 themes/theme1.jar /opt/keycloak/providers/
COPY --chown=keycloak:keycloak --chmod=644 themes/theme2.jar /opt/keycloak/providers/

# Compilando a imagem customizada do Keycloak
RUN /opt/keycloak/bin/kc.sh build

# Etapa final da imagem
FROM registry.redhat.io/rhbk/keycloak-rhel9:26.2-15

# Copiando o resultado do build
COPY --from=builder /opt/keycloak/ /opt/keycloak/

# Definindo ponto de entrada padrão
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
