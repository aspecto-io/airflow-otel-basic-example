from tracing import setup_otel
from opentelemetry import trace
setup_otel()

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

from datetime import datetime
import requests

# add requests instrumentation
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

with DAG("otel_dag", start_date=datetime(2023,1,1), schedule_interval="@daily", catchup=False) as dag:
    def print_hello():
        print('setup opentelemetry')
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("airflow span") as span:
            print("Doing work")
            requests.get('https://w3schools.com/python/demopage.htm')

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=print_hello,
    )

    task_http_sensor_check = HttpSensor(
        task_id="http_sensor_check",
        http_conn_id="http_default",
        endpoint="http",
        request_params={},
        response_check=lambda response: "httpbin" in response.text,
        poke_interval=5,
        dag=dag,
    )

    python_task >> task_http_sensor_check
