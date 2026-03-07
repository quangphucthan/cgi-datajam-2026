# CGI-DATAJAM-2026

Full-stack triage assistant with:
- `frontend`: React + Vite (`http://localhost:5173`)
- `backend`: FastAPI (`http://localhost:8000`)
- `n8n`: webhook workflow orchestration

## Architecture

1. User enters symptoms in chat.
2. Frontend calls backend `POST /api/triage` with:
```json
{ "text": "..." }
```
3. Backend forwards request to `N8N_WEBHOOK_URL`.
4. n8n workflow calls backend `POST /predict` to get CTAS + advice.
5. n8n returns final JSON to backend.
6. Backend passes n8n response back to frontend.
7. Frontend renders `reply` (or falls back to parsed output text).

## API Endpoints

- `GET /`  
Health check.

- `POST /api/triage`  
Input:
```json
{ "text": "chest pain and sweating" }
```
Behavior: forwards input to n8n webhook and returns n8n JSON.

- `POST /predict`  
Input:
```json
{
  "symptoms": ["chest pain", "sweating"],
  "location": "Halifax"
}
```
Output:
```json
{
  "predicted_ctas": 1,
  "advice": "Go to the Emergency Room immediately!",
  "location": "Halifax"
}
```

## Project Structure

```text
CGI-DATAJAM-2026/
├── README.md
├── backend/
│   ├── main.py
│   ├── triage_api.py
│   ├── requirements.txt
│   ├── .env
│   ├── .envSample
│   ├── services/
│   ├── data/
│   ├── graphs/
│   └── scripts/
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── components/
        └── services/
```

## Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set webhook URL:
```bash
export N8N_WEBHOOK_URL="http://localhost:5678/webhook-test/triage"
```

Or load from file:
```bash
source .env
```

Run:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Optional frontend env override:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## n8n Workflow Notes

- Webhook path should match your `N8N_WEBHOOK_URL`.
- For `/webhook-test/...`, keep workflow in test listening mode.
- For production use `/webhook/...` and activate workflow.
- n8n workflow should call backend `POST http://127.0.0.1:8000/predict`.

Expected webhook response should include readable text in one of:
- `reply` (preferred)
- `output`
- `message`
- `text`

## Troubleshooting

- `500 N8N_WEBHOOK_URL is not configured`: `.env` not loaded in backend shell.
- `502 Bad Gateway`: backend cannot reach n8n, n8n returned non-200, or n8n returned non-JSON.
- `404 /predict` in n8n: restart backend and confirm it is running updated `backend/main.py`.
- Unexpected CTAS level: inspect `symptoms` payload sent to `/predict`.

## Presentation

- Google Doc: https://docs.google.com/document/d/1rTAWS2ZlLqejZ_N--YHcUeTFSFsZyDoUjbXxxXjxA-A/edit?tab=t.0
- Slides: https://docs.google.com/presentation/d/1r34S6yu0ylaaLeQ5pBjz2kyg70In4kEbHobScx5y_ko/edit?slide=id.g3c55df61ae3_0_12#slide=id.g3c55df61ae3_0_12
- Demo: https://www.youtube.com/watch?v=q1-4X3uDSH0
