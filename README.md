# AI-Based Smart Governance and Compliance Monitoring System for Coal Mines

**SIH Problem Statement:** SIH26024 | **Demo:** MineSafe governance console

This repository contains a responsive React, Vite and TypeScript demonstration. It runs without a backend: fictional operational records are stored in the browser's `localStorage`. It does not connect to real mine sensors or worker tracking.

## Run locally

Requirements: Node.js 18+ and npm.

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Run `npm run build` to create the deployable production bundle in `frontend/dist`.

On Windows, `start-dev.bat` opens the frontend development server for you.

## Deploy to Vercel

Import this GitHub repository. Vercel uses the root `vercel.json` to install and build the frontend and to route nested React Router paths back to the SPA. No backend URL, environment variables, or API keys are required.

## Prototype features

- Eleven routed command-centre sections with responsive layouts
- Overview KPIs, sensor cards, charts, tunnel risk table and activity summaries
- Simulated sensor readings that update while the demo is running, with pause/resume and breach controls
- Interactive SVG tunnel schematic, risk and alert register, hazard workflow, worker directory, inspections, compliance checklist and reports
- In-browser record persistence, notifications, CSV export, and print-to-PDF

## Demo and safety notice

All mine names, workers, readings, thresholds, reports and operational records are fictional. Thresholds are illustrative and are not approved operating limits. This software does not track physical workers, connect to certified instruments, predict accidents, certify statutory compliance, or send SMS, email, WhatsApp, push or emergency messages.

The `backend/` directory is retained as earlier prototype code and is not required by the current frontend demo.
