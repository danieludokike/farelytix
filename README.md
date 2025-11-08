# ✈️ Farelytix — Intelligent Flight Price Monitoring & Forecasting System

**Farelytix** is a smart, data-driven platform that tracks, analyzes, and predicts flight prices in real time.  
It collects airfare data (from APIs or simulated inputs), stores it in a structured database, and applies lightweight forecasting to visualize price trends and volatility.

This is the **MVP (Minimum Viable Product)** version — built entirely in **Python** with a **FastAPI backend** and an interactive **Streamlit dashboard** for visualization.


## 🚀 Features

- 🧭 **Flight Price Tracking (Simulated or via API)**
  - Define flight routes and providers, then fetch or simulate live ticket data.
  - Data is stored automatically in a structured SQLite database.

- 📊 **Historical Data Storage**
  - Keeps a complete record of flight price snapshots per route and provider.

- 🤖 **Price Forecasting**
  - Uses a simple pure-Python moving-average + drift model to forecast short-term prices.
  - Forecasts include upper/lower confidence bounds.

- 📈 **Interactive Dashboard**
  - Built with **Streamlit** and **Plotly**.
  - Displays live prices, trends, volatility metrics, and forecast curves.

- 🧩 **Extensible Architecture**
  - Easily integrate real Flight APIs (Amadeus, Kiwi, Skyscanner, etc.).
  - Forecasting model can be upgraded to Prophet, LightGBM, or LSTM.
  - Modular design — backend and dashboard are independent but connected via API.


## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend API** | FastAPI, SQLAlchemy, Pydantic |
| **Database** | SQLite (local) |
| **Frontend / Dashboard** | Streamlit + Plotly |
| **Forecasting** | Custom Python logic (Mean + Drift) |
| **Optional Integration** | Flight Ticket APIs (Amadeus / Kiwi / Skyscanner) |
| **Language** | Python 3.10+ |


## 🧩 Project Structure
```
Farelytix/
├─ backend/
│ └─ app/
│ ├─ main.py # FastAPI entrypoint
│ ├─ db.py # SQLAlchemy DB engine
│ ├─ models.py # ORM models
│ ├─ schemas.py # Pydantic models
│ ├─ crud.py # Database operations
│ ├─ services/
│ │ └─ forecast.py # Forecasting logic
│ └─ api/
│ ├─ tracked_search.py # Route creation/list API
│ └─ prices.py # Price history + forecast API
├─ dashboard/
│ └─ app_streamlit.py # Streamlit dashboard UI
├─ scripts/
│ └─ seed_demo_data.py # Generates sample DB data
├─ requirements.txt
└─ run_dev.sh # Run API + dashboard together
```

## 🧰 Local Development Setup

### 1️⃣ Clone and setup environment
```bash
git clone https://github.com/danieludokike/farelytix.git
cd farelytix
python -m venv env
source env/bin/activate      # or .\env\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```
### 2️⃣ Seed demo data (optional)
```bash
python -m scripts.seed_demo_data
```
This creates farelytix.db and seeds it with demo price data.

### 3️⃣ Start the backend API
```bash
uvicorn backend.app.main:app --reload --port 8000
Visit: http://127.0.0.1:8000/docs
```

### 4️⃣ Launch the dashboard
In another terminal:

```bash
streamlit run dashboard/app_streamlit.py
Visit: http://localhost:8501
```

### 5️⃣ Run both together (optional)
```bash
./run_dev.sh
🔁 Example API Responses
GET /api/prices/{tracked_id}
json
{
  "id": "c86093c6-5152-45b2-9f45-6590c80194da",
  "currency": "USD",
  "series": [
    {"ds": "2025-11-01T00:00:00Z", "price": 340.00},
    {"ds": "2025-11-03T00:00:00Z", "price": 330.00}
  ],
  "forecast": [
    {"ds": "2025-11-09T00:00:00Z", "yhat": 335.0, "yhat_lower": 320.0, "yhat_upper": 350.0}
  ]
}
POST /api/prices/dev/random-snapshot/{tracked_id}
Adds a random price snapshot (for demo purposes).

🧠 How It Works
Tracked Search Creation
User defines a flight route (origin → destination, provider, etc.).

Snapshot Generation
Either simulate new snapshots via the /dev/random-snapshot endpoint
or fetch real data from a flight ticket API (Amadeus, Kiwi, etc.).

Data Storage
Each snapshot is stored in SQLite via SQLAlchemy.

Forecast Engine
The backend computes a simple 3-day forecast using the last price trend.

Visualization Layer
Streamlit dashboard fetches API data, plots history + forecast in real time.

🧠 Coming Next
🌐 Integration with real flight APIs (Amadeus, Kiwi, Skyscanner)

🔮 Advanced forecasting (Prophet, LightGBM, LSTM)

🔔 Price alerts via email or Telegram

🐳 Docker containerization

📊 Data analytics dashboard for historical trends

🧑‍💻 Author
Ikegbunam Daniel
Founder, SkillRover Technologies
Python Developer | Backend Engineer | Tech Educator

📍 Nigeria
https://github.com/danieludokike/