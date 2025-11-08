import time
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Farelytix Dashboard", layout="wide")
st.title("✈️ Farelytix — Python Dashboard")

API_BASE = st.sidebar.text_input("API Base URL", value="http://127.0.0.1:8000").rstrip("/")
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=False)
refresh_sec = st.sidebar.number_input("Refresh (s)", 5, 300, 20, 5)

def api_get(path):
    try:
        r = requests.get(API_BASE + path, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"GET {path} failed: {e}")
        return None

def api_post(path, json=None):
    try:
        r = requests.post(API_BASE + path, json=json, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"POST {path} failed: {e}")
        return None

# Create tracked search
with st.expander("Create a new tracked search"):
    c1, c2, c3 = st.columns(3)
    with c1: origin = st.text_input("Origin (IATA)", "LGA")
    with c2: destination = st.text_input("Destination (IATA)", "LHR")
    with c3: provider = st.text_input("Provider", "DemoProvider")
    if st.button("Create"):
        resp = api_post("/api/tracked-search", {"origin": origin, "destination": destination, "provider": provider})
        if resp: st.success(f"Created: {resp['id']}"); st.rerun()

# List tracked
tracked = api_get("/api/tracked-search") or []
if not tracked:
    st.info("No tracked searches yet. Create one above or run the seed script.")
    st.stop()

options = {f"{t['origin']} → {t['destination']} | {t.get('provider','')} · {t['id']}": t["id"] for t in tracked}
label = st.selectbox("Choose a tracked search", list(options.keys()))
tracked_id = options[label]

# Load series
payload = api_get(f"/api/prices/{tracked_id}")
if not payload: st.stop()

series = pd.DataFrame(payload.get("series", []))
fc = pd.DataFrame(payload.get("forecast", []))
if not series.empty: series["ds"] = pd.to_datetime(series["ds"])

# Stats
if not series.empty:
    window = min(30, len(series))
    min_30 = series["price"].tail(window).min()
    mean_30 = series["price"].tail(window).mean()
    vol_30 = series["price"].tail(window).std(ddof=0) if window > 1 else 0.0
    last_price = series["price"].iloc[-1]
else:
    min_30 = mean_30 = vol_30 = last_price = None

c1, c2, c3, c4 = st.columns(4)
c1.metric("Last Price", f"{last_price if last_price is not None else '—'} {payload.get('currency','USD')}")
c2.metric("30D Min", f"{round(min_30,2) if min_30 is not None else '—'}")
c3.metric("30D Mean", f"{round(mean_30,2) if mean_30 is not None else '—'}")
c4.metric("30D Vol", f"{round(vol_30,2) if vol_30 is not None else '—'}")

# Chart
fig = go.Figure()
if not series.empty:
    fig.add_trace(go.Scatter(x=series["ds"], y=series["price"], name="Historical", mode="lines+markers"))
if not fc.empty and {"ds","yhat","yhat_lower","yhat_upper"}.issubset(fc.columns):
    x_band = list(fc["ds"]) + list(fc["ds"][::-1])
    y_band = list(fc["yhat_upper"]) + list(fc["yhat_lower"][::-1])
    fig.add_trace(go.Scatter(x=x_band, y=y_band, fill="toself", name="Confidence", line=dict(width=0), hoverinfo="skip", opacity=0.2))
    fig.add_trace(go.Scatter(x=fc["ds"], y=fc["yhat"], name="Forecast", mode="lines", line=dict(dash="dash")))
fig.update_layout(title="Fare over time", xaxis_title="Date", yaxis_title=f"Price ({payload.get('currency','USD')})", margin=dict(t=50,l=60,r=20,b=50))
st.plotly_chart(fig, use_container_width=True)

# Dev: add random point
if st.button("➕ Generate Random Price Snapshot (DEV)"):
    resp = api_post(f"/api/prices/dev/random-snapshot/{tracked_id}")
    if resp: st.success("Added."); st.rerun()

# Auto refresh
if auto_refresh:
    st.caption(f"Auto refresh every {refresh_sec} seconds…")
    time.sleep(int(refresh_sec))
    st.rerun()
