# A versão do builder, Operator e CR deve avançar em conjunto.
ARG KEYCLOAK_VERSION=26.6.4
ARG PYROSCOPE_JAVA_AGENT_VERSION=2.8.0

FROM registry.access.redhat.com/ubi9/ubi-minimal:9.6 AS pyroscope-agent
ARG PYROSCOPE_JAVA_AGENT_VERSION
ADD --chmod=0444 https://github.com/grafana/pyroscope-java/releases/download/v${PYROSCOPE_JAVA_AGENT_VERSION}/pyroscope.jar /tmp/pyroscope.jar

FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS builder

# Opções de build: PostgreSQL, health, métricas, tracing e event metrics.
ENV KC_DB=postgres \
    KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=true \
    KC_TRACING_ENABLED=true \
    KC_FEATURES=opentelemetry,user-event-metrics\
    KC_EVENT_METRICS_USER_ENABLED=true \
    KC_TRACING_SAMPLER_TYPE=traceidratio

COPY --chown=keycloak:keycloak --chmod=644 themes/rhbk-theme-botelho-1.2.2.jar /opt/keycloak/providers/

# Evita falso positivo de alteração do provider no start --optimized.
RUN touch -m --date=@1743465600 /opt/keycloak/providers/* && \
    /opt/keycloak/bin/kc.sh build

ARG KEYCLOAK_VERSION=26.6.4
ARG PYROSCOPE_JAVA_AGENT_VERSION=2.8.0
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}

ARG KEYCLOAK_VERSION
ARG PYROSCOPE_JAVA_AGENT_VERSION
LABEL org.opencontainers.image.title="Keycloak customizado" \
      org.opencontainers.image.version="${KEYCLOAK_VERSION}" \
      org.opencontainers.image.description="Keycloak com temas customizados, métricas, tracing e Pyroscope Java agent ${PYROSCOPE_JAVA_AGENT_VERSION}" \
      org.opencontainers.image.source="https://github.com/thiagobotelho/keycloak-gitops"

COPY --from=builder /opt/keycloak/ /opt/keycloak/
COPY --from=pyroscope-agent --chown=keycloak:keycloak /tmp/pyroscope.jar /opt/keycloak/pyroscope.jar

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
