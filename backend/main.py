import json
import os
from urllib import error, request

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TriageRequest(BaseModel):
    text: str = Field(min_length=1)


class PredictResponse(BaseModel):
    predicted_ctas: int
    advice: str
    location: str | None = None


CTAS_RECOMMENDATION = {
    1: "Go to the Emergency Room immediately!",
    2: "Go to the Emergency Room as soon as possible.",
    3: "Visit a clinic for urgent care.",
    4: "You can go to a clinic or urgent care center.",
    5: "You can manage at home or visit a pharmacy.",
}


def infer_ctas_from_symptoms(symptoms: list[str]) -> int:
    lowered = {s.lower().strip() for s in symptoms}

    if ("chest pain" in lowered and "profuse sweating" in lowered) or (
        "shortness of breath" in lowered and "chest pain" in lowered
    ):
        return 1

    if ("chest pain" in lowered and "vomiting" in lowered) or (
        "head injury" in lowered and "dizziness" in lowered
    ):
        return 2

    if lowered.intersection({"severe pain", "high fever", "vomiting", "infection"}):
        return 3

    if lowered.intersection({"rash", "sprain", "mild fever", "cold", "cough"}):
        return 4

    return 5


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.post("/api/triage")
def triage(input_data: TriageRequest):
    text = input_data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    webhook_url = os.getenv("N8N_WEBHOOK_URL", "").strip()
    if not webhook_url:
        raise HTTPException(status_code=500, detail="N8N_WEBHOOK_URL is not configured")
    payload = json.dumps({"text": text}).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {"reply": ""}
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise HTTPException(status_code=502, detail=f"n8n HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"Failed calling n8n webhook: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="n8n returned non-JSON response") from exc


@app.post("/predict", response_model=PredictResponse)
def predict(data: dict):
    symptoms = data.get("symptoms", [])
    if isinstance(symptoms, str):
        symptoms = [symptoms]
    if not isinstance(symptoms, list):
        symptoms = []

    location = data.get("location")
    ctas_level = infer_ctas_from_symptoms([str(s) for s in symptoms])

    return PredictResponse(
        predicted_ctas=ctas_level,
        advice=CTAS_RECOMMENDATION[ctas_level],
        location=str(location) if location is not None else None,
    )
