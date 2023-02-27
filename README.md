# airflow-otel-basic-example

In `dags/tracing.py`, replace "your-aspecto-token" with your account token [from here](https://app.aspecto.io/integration/tokens)

Then run

```bash
docker compose build
docker compose up
```

And run "otel_dag", you should be able to see traces in aspecto.

This repo demonstrate creating manual spans in a python operator:
```py
with tracer.start_as_current_span("airflow span") as span:
    print("Doing work")
    requests.get('https://w3schools.com/python/demopage.htm')
```

And auto instrumentating the `request` library
