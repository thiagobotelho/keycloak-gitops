# A versão do builder, Operator e CR deve avançar em conjunto.
ARG KEYCLOAK_VERSION=26.6.4
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS builder

# Opções de build: PostgreSQL, health, métricas, tracing e event metrics.
ENV KC_DB=postgres \
    KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=true \
    KC_TRACING_ENABLED=true \
    KC_FEATURES=opentelemetry,user-event-metrics\
    KC_EVENT_METRICS_USER_ENABLED=true \
    KC_TRACING_SAMPLER_TYPE=traceidratio

COPY --chown=keycloak:keycloak --chmod=644 themes/theme1.jar /opt/keycloak/providers/
COPY --chown=keycloak:keycloak --chmod=644 themes/theme2.jar /opt/keycloak/providers/

# Evita falso positivo de alteração do provider no start --optimized.
RUN touch -m --date=@1743465600 /opt/keycloak/providers/* && \
    /opt/keycloak/bin/kc.sh build

ARG KEYCLOAK_VERSION=26.6.4
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}

ARG KEYCLOAK_VERSION
LABEL org.opencontainers.image.title="Keycloak customizado" \
      org.opencontainers.image.version="${KEYCLOAK_VERSION}" \
      org.opencontainers.image.source="https://github.com/thiagobotelho/keycloak-gitops"

COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
