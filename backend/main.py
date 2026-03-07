import json
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


class TriageResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.post("/api/triage", response_model=TriageResponse)
def triage(input_data: TriageRequest):
    text = input_data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    debug_payload = {
        "received_text": text,
        "debug": True,
    }
    return TriageResponse(reply=json.dumps(debug_payload))
