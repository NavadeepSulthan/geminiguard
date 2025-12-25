from fastapi import FastAPI
import time
import os
from datadog import initialize, api

# =====================================================
# Datadog Initialization (AGENTLESS, us5 REGION)
# =====================================================
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

if not DD_API_KEY or not DD_APP_KEY:
    raise RuntimeError(
        "Datadog keys missing. "
        "Set DD_API_KEY and DD_APP_KEY as environment variables."
    )

options = {
    "api_key": DD_API_KEY,
    "app_key": DD_APP_KEY,
    # IMPORTANT: your account is us5
    "api_host": "https://api.us5.datadoghq.com"
}

initialize(**options)

# =====================================================
# FastAPI App
# =====================================================
app = FastAPI(title="GeminiGuard")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-metric")
def test_metric():
    """
    Sends a custom metric to Datadog using the HTTP API.
    No agent required.
    """
    timestamp = int(time.time())

    # ---- Send request count ----
    api.Metric.send(
        metric="geminiguard.request.count",
        points=[(timestamp, 1)],
        tags=[
            "env:local",
            "service:geminiguard",
            "endpoint:test-metric"
        ]
    )

    # ---- Send latency metric ----
    latency = 0.2
    api.Metric.send(
        metric="geminiguard.latency.seconds",
        points=[(timestamp, latency)],
        tags=[
            "env:local",
            "service:geminiguard"
        ]
    )

    return {
        "message": "Metrics sent to Datadog (us5)",
        "timestamp": timestamp
    }
