# AI-Based Smart Governance and Compliance Monitoring System for Coal Mines

**SIH Problem Statement:** SIH26024
**Application:** CollieryOS demonstration command centre

This repository contains a React + Vite + TypeScript frontend and a FastAPI + SQLAlchemy + SQLite backend. All mine names, workers, sensor readings, thresholds, reports, and operational records are fictional. The app is a hackathon demonstration and is not an operational safety system or regulatory certification.

## Requirements

- Node.js 18+ and npm
- Python 3.10+

## Run the backend (Terminal 1)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

On macOS/Linux activate with `source venv/bin/activate`.

## Run the frontend (Terminal 2)

```powershell
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173
- Backend health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

SQLite data is stored at `backend/data/governance.db`. Tables are created and demo records seeded on first startup; user updates persist across refreshes and backend restarts. The database file is excluded from version control.

## Windows convenience launcher

Run `start-dev.bat` from the repository root to open separate backend and frontend terminal windows. The launcher expects Node.js and Python installed; it creates the backend venv and installs requirements the first time.

## Deploy the frontend on Vercel

The root `vercel.json` builds the React app from `frontend/`, publishes `frontend/dist`, and sends SPA routes to `index.html`. Connect the repository and deploy from the `main` branch. Set `VITE_API_URL` in Vercel to the base URL of a publicly reachable backend API (ending in `/api`) before redeploying; the local default `http://localhost:8000/api` only works on the developer's machine. The FastAPI backend and SQLite database need a separate host with persistent storage; this Vercel configuration deploys the frontend only.

For a demo backend, `render.yaml` defines a Render FastAPI web service and PostgreSQL database. In Render, create a Blueprint from this repository and apply the `render.yaml`. After it is live, copy the service's `onrender.com` origin into Vercel's `VITE_API_URL` as `https://<service>.onrender.com/api`, then redeploy the frontend. The Blueprint uses Render's free Postgres plan, which expires after 30 days; choose durable hosted storage for a long-lived deployment. Free Render web services can spin down while idle; the frontend allows up to 75 seconds for production API requests to accommodate a cold start. When the frontend is built for production without `VITE_API_URL`, it no longer tries to contact the visitor's own `localhost`; it shows this deployment instruction instead.

## Main features

- Eleven routed command-centre sections with responsive desktop and mobile layouts
- SQLite-backed overview, fictional workforce directory, tunnel schematic, sensor channels, hazard workflow, alerts, inspections, compliance checklist, notification feed, activity log, and reports
- Live-style sensor simulation updates every five seconds, with pause/resume, reset, configurable illustrative thresholds shown in the interface, and a demo threshold-breach workflow
- Breach workflow updates tunnel risk, sensor state, alert, in-app notification, reading history, and activity log in the database
- Hazard and inspection creation, status transitions, alert acknowledge/assign/escalate/resolve, editable illustrative sensor thresholds, compliance document uploads, notification read state, CSV downloads for operational tables, and print-to-PDF reports
- API-unavailable state with an explicit retry action; the frontend does not substitute mock operational API responses

## Configuration

Copy `backend/.env.example` to `backend/.env` to override `DATABASE_URL`. Frontend API base URL defaults to `http://localhost:8000/api`; set `VITE_API_URL` in `frontend/.env` to override it.

## Safety and privacy boundary

No physical sensors, GPS tracking, SMS, WhatsApp, push messaging, statutory submissions, accident prediction, or certified safety controls are implemented. Real mine use requires certified instrumentation, validated limits, approved operational procedures, and safety testing.
