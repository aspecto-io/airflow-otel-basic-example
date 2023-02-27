from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

def setup_otel():
    resource = Resource(attributes={
        SERVICE_NAME: "airflow-playground"
    })
    aspectoToken = "your-aspecto-token"
    headers = f"Authorization={aspectoToken}"

    provider = TracerProvider(resource=resource)
    aspecto_exporter = OTLPSpanExporter(endpoint="https://otelcol.aspecto.io:4317", headers=headers)
    processor = SimpleSpanProcessor(aspecto_exporter)
    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)
