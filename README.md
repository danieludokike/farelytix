# Farelytix — Intelligent Flight Price Monitoring & Forecasting System

**Farelytix** is a smart, data-driven platform that tracks, analyzes, and predicts flight prices in real time.  
It automatically scrapes airfare data, stores it in a structured database, and applies forecasting models to detect price trends and alert users before prices rise or drop.

Built with **FastAPI**, **Playwright**, **PostgreSQL**, and **Plotly**, Farelytix combines backend engineering, data processing, and machine learning in one cohesive system.

---

## 🚀 Features

- 🧭 **Automated Flight Price Tracking**
  - Periodically scrapes prices for user-defined routes and dates from supported travel providers.

- 📊 **Historical Data Storage**
  - Maintains a complete time-series history of price changes and flight metadata.

- 🤖 **Price Forecasting**
  - Uses Prophet and other ML models to forecast short-term price trends with confidence intervals.

- 🔔 **Smart Alerts**
  - Notifies users when price thresholds or forecast-based signals are triggered (email, Telegram, etc.).

- 📈 **Interactive Visualization**
  - Simple frontend powered by **Plotly.js** to visualize price trends, forecasts, and volatility over time.

- 🧩 **Modular Architecture**
  - Separated services for API, scrapers, background workers, and UI—each containerized and easy to scale.


## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **API / Backend** | FastAPI, SQLAlchemy, Pydantic |
| **Scraping** | Playwright (headless Chromium) |
| **Database** | PostgreSQL (TimescaleDB optional) |
| **Background Jobs** | Celery + Redis |
| **Forecasting / ML** | Prophet, scikit-learn, pandas |
| **Visualization** | Plotly.js (frontend) |
| **Containerization** | Docker, Docker Compose |
| **Deployment** | Render / Railway / AWS / DigitalOcean |

---

## Data Flow Overview

1. **Tracked Search Creation**  
   User defines a route (origin → destination), provider, and date range.

2. **Scheduler / Worker Trigger**  
   Celery or cron schedules scraping jobs periodically.

3. **Scraping Layer**  
   Playwright opens provider pages, extracts price info, and saves structured snapshots.

4. **ETL & Database Storage**  
   Snapshots are normalized and stored in PostgreSQL.

5. **Forecast Engine**  
   Daily jobs use Prophet or ML models to forecast next 7–14 days of prices.

6. **Signal & Alerts Engine**  
   Detects opportunities (price drops or forecasted hikes) and notifies users.

7. **Visualization Layer**  
   Frontend (Plotly.js) fetches from FastAPI and displays interactive charts and metrics.

---

## Example API

### `GET /api/prices/{tracked_id}`
```json
{
  "id": "demo-route-nyc-lhr",
  "currency": "USD",
  "series": [
    {"ds":"2025-10-01","price":320.00},
    {"ds":"2025-10-05","price":310.00}
  ],
  "forecast": [
    {"ds":"2025-10-11","yhat":305.0,"yhat_lower":290.0,"yhat_upper":320.0}
  ]
}
POST /api/tracked-search
json

{
  "origin": "LGA",
  "destination": "LHR",
  "depart_date": "2026-01-15",
  "provider": "ProviderX"
}
🧰 Local Development Setup
1. Clone and setup environment
bash

git clone https://github.com/danieludokike/farelytix.git
cd farelytix
cp .env
2. Run with Docker (recommended)
bash

docker compose -f infra/docker-compose.yml up --build
This spins up:

PostgreSQL

Redis

FastAPI backend

Scraper workers

Frontend static UI

3. Run backend manually (alternative)
bash

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
4. Open frontend
Open frontend/static/index.html in your browser or run:

bash

cd frontend/static
python -m http.server 8080
Then visit: http://localhost:8080

🧪 Testing
bash

pytest tests/ --maxfail=1 --disable-warnings -q
Unit tests for scrapers (HTML parsing).

Integration tests for FastAPI endpoints (uses a test DB).

📦 Deployment
Farelytix can be deployed using any modern container platform:

Render / Railway → simple Docker deployment

AWS ECS / EC2 → production ready

Vercel (for frontend only)

GitHub Actions → for CI/CD & image build automation

🧩 Roadmap
 Multi-provider scraping integration

 Authentication & user dashboards

 Telegram & email alerting

 Advanced forecasting (LightGBM / LSTM)

 Data analytics API for partners

 Cloud deployment templates (AWS / Railway)

🧠 About the Project
Farelytix is part of an ongoing personal initiative to build full-stack, data-intensive applications that combine backend engineering, data analytics, and automation.
It demonstrates practical skills in web scraping, data pipeline design, ML forecasting, and backend architecture — all built with clean, testable Python code.

🧑‍💻 Author
Udokike Daniel
Founder, SkillRover Technologies
Python Developer | Backend Engineer | Tech Educator