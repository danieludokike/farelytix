
from datetime import timedelta

def simple_forecast(series, horizon: int = 7):
    """
    Simple pure-Python forecast used for MVP.
    - series: list[dict] with keys 'ds' (datetime) and 'price' (float)
    - horizon: number of days to forecast
    Returns: list[dict] with keys 'ds','yhat','yhat_lower','yhat_upper'
    """
    # defensive checks
    if not series:
        return []

    # Ensure series sorted by date ascending
    try:
        series = sorted(series, key=lambda x: x["ds"])
    except Exception:
        # if ds values are strings, attempt to leave as-is (caller should pass datetimes)
        pass

    # last price and simple drift
    last_price = float(series[-1]["price"])
    if len(series) >= 2:
        try:
            drift = float(series[-1]["price"]) - float(series[-2]["price"])
        except Exception:
            drift = 0.0
    else:
        drift = 0.0

    # baseline mean of up-to-7 last points
    window = min(7, len(series))
    mean = sum(float(p["price"]) for p in series[-window:]) / window

    forecast = []
    last_date = series[-1]["ds"]
    for i in range(1, horizon + 1):
        ds = last_date + timedelta(days=i)
        yhat = mean + drift * i
        spread = max(5.0, abs(yhat) * 0.10)
        forecast.append({
            "ds": ds,
            "yhat": round(yhat, 2),
            "yhat_lower": round(yhat - spread, 2),
            "yhat_upper": round(yhat + spread, 2)
        })
    return forecast
